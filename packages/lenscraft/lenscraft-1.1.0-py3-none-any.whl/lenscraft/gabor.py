import cv2
import numpy as np
import shapely


class FeatureMap:
    def __init__(self, features):
        """Features (width x height x features)"""
        self.features = features
        self.normalized = self._normalize(features)
        self.F = features.shape[2]

        print("Create feature map: ", features.shape)

    def get_feature_vector_at(self, x, y):
        # Extract the feature vector for the given pixel
        f = self.normalized[y, x, :]

        return f

    def get_feature_area(self, x, y, padding=10):
        f = self.normalized[y - padding : y + padding, x - padding : x + padding, :]
        f = f.reshape(((padding * 2) ** 2, self.F))
        return f

    def get_polygon_area(self, polygon, sample=None):
        features = []
        # Iterate over the pixels within the bounding box
        minx, miny, maxx, maxy = polygon.bounds
        for y in range(int(miny), int(maxy)):
            for x in range(int(minx), int(maxx)):
                point = shapely.Point(x, y)
                # Check if the point is within the image
                if x < 0 or x >= self.normalized.shape[1]:
                    continue
                if y < 0 or y >= self.normalized.shape[0]:
                    continue
                # Check if the point is within the polygon
                if not polygon.contains(point):
                    continue

                features.append(self.get_feature_vector_at(x, y))

        result = np.array(features)
        if sample is not None:
            N = result.shape[0]  # Number of features
            M = min(sample, N)  # Requested sample size
            random_indices = np.random.choice(N, M, replace=False)
            result = result[random_indices, :]

        return result

    def all(self):
        h, w = self.normalized.shape[0:2]
        return self.normalized.reshape((w * h, self.F))

    def flat_shape(self):
        h, w = self.normalized.shape[0:2]
        return (w, h)

    def _normalize(self, features):
        # Compute min and max for each feature across all pixels
        min_vals = np.min(features, axis=(0, 1))
        max_vals = np.max(features, axis=(0, 1))

        # Ensure we don't divide by zero if a feature has constant value by setting those to 1
        denom = np.where(max_vals - min_vals != 0, max_vals - min_vals, 1)

        # Normalize each feature separately
        normalized = (features - min_vals) / denom

        return normalized


class Gabor:
    def __init__(self):
        self.kernels = build_gabor_kernels()

    def apply_gabor_filters(self, img):
        return np.array([cv2.filter2D(img, cv2.CV_32F, k) for k in self.kernels])

    def load_features(self, image_path) -> FeatureMap:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.generate_features(img)

    def generate_features(self, img):
        features = self.apply_gabor_filters(img).transpose((1, 2, 0))

        # Add color info as a feature
        # features = np.concatenate((features, img), axis=0)
        grayscale_feature = np.expand_dims(img, axis=2)
        print("feature shape: ", grayscale_feature.shape, features.shape)
        all_features = np.concatenate((features, grayscale_feature), axis=2)

        return FeatureMap(all_features)


def build_gabor_kernels(
    ksize=41,
    sigmas=[11, 21],
    thetas=np.arange(0, np.pi, np.pi / 4),
    lambdas=[5, 10, 20],
    gamma=0.5,
    psi=0,
):
    kernels = []
    for theta in thetas:
        for sigma in sigmas:
            for lambd in lambdas:
                kernel = cv2.getGaborKernel(
                    (ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F
                )
                kernels.append(kernel)
    return kernels


def apply_gabor_filters(img, kernels):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if necessary
    feature_vectors = []
    for kernel in kernels:
        filtered = cv2.filter2D(img, cv2.CV_8UC3, kernel)
        feature_vectors.append(filtered.reshape(-1))
    return np.array(
        feature_vectors
    ).T  # Transpose to make it (num_pixels, num_features)


def apply_gabor_filters(img, kernels):
    # Apply Gabor filters to the image
    feature_maps = np.array([cv2.filter2D(img, cv2.CV_32F, k) for k in kernels])
    return feature_maps


def extract_features(feature_maps, mask):
    # Use the mask to extract features from the ROI
    masked_features = feature_maps[:, mask > 0]  # Apply mask to each feature map
    # You can average (or otherwise pool) the features within the ROI if needed
    roi_features = np.mean(masked_features, axis=1)
    return roi_features

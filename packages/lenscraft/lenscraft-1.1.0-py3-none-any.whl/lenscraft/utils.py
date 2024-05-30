import threading
import nanoid

ID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ID_SIZE = 6

def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            
            if hasattr(debounced, '_timer'):
                debounced._timer.cancel()
            
            debounced._timer = threading.Timer(wait, call_it)
            debounced._timer.start()
        
        return debounced
    return decorator

def uid() -> str:
    """Returns a string that is likely to be unique.
    Works well if you are generating hundreds or maybe thousands of ids.
    If you need millions of ids, do something else
    """
    return nanoid.generate(ID_ALPHABET, 6)
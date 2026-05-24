from functools import wraps
def log_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🤩 Function {func.__name__} started.")
        result = func(*args, **kwargs)
        print(f"🥸 Function {func.__name__} finished.")
        return result
    return wrapper

@log_activity
def brew_chai(type, milk="no"):
    print(f"Brew chai of {type} and milk status is {milk}.")

brew_chai("Masala", milk="no")
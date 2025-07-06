import importlib

def execute_action(action_name, row):
    """
    Loads the module named by `action_name` from the `actions` package
    and runs its `execute()` method with the provided row.
    """
    try:
        module = importlib.import_module(f"actions.{action_name}")
        return module.execute(row)
    except ModuleNotFoundError:
        return f"[ERROR] Action module 'actions.{action_name}' not found."
    except AttributeError:
        return f"[ERROR] 'execute' function not defined in actions.{action_name}."
    except Exception as e:
        return f"[ERROR] Exception while running {action_name}: {str(e)}"

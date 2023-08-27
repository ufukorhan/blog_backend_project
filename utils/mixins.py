__author__ = "Ufuk Orhan"

def check_viewset_methods(viewset_class, http_methods): # NoQA
    """
    Check if the provided ClassViewSet has the required methods for the
     specified HTTP methods.

    :param viewset_class: The ClassViewSet class to be checked.
    :type viewset_class: class

    :param http_methods: A list of HTTP methods for which corresponding viewset
     methods are required.
    :type http_methods: list of str

    :return: True if the ClassViewSet has the required methods for the
     specified HTTP methods, False otherwise.
    :rtype: bool
    """
    http_methods_to_test = {
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
        "post": "create",
        "get": "list"
    }

    replaced_http_methods = []
    for http_method in http_methods:
        view_method_name = http_methods_to_test.get(http_method)
        if not view_method_name:
            raise ValueError(f"Invalid HTTP method: {http_method}")

        view_method = getattr(viewset_class, view_method_name, None)
        if not view_method or not callable(view_method):
            return False

        replaced_http_methods.append(view_method.__name__)

    all_view_methods = []
    for http_method in http_methods_to_test.values():
        view_method = getattr(viewset_class, http_method, None)
        if not view_method or not callable(view_method):
            continue
        all_view_methods.append(view_method.__name__)

    return set(replaced_http_methods) == set(all_view_methods)

def required_test_methods(
        http_methods,
        class_view_set,
):
    """
    Decorator to enforce the presence of specific test methods within a test
     class based on the provided HTTP methods.

    :param http_methods: A list of HTTP methods for which corresponding test
     methods are required within the decorated class.
    :type http_methods: list of str

    :param class_view_set: The ClassViewSet to be associated with the decorated
     test class.
    :type class_view_set: class

    :return: The decorated test class with enforced test methods.
    :rtype: class
    """
    if http_methods == "all":
        http_methods = ["put", "patch", "delete", "post", "get"]

    def decorator(cls):
        http_methods_to_test = {
            "put": "perform_update",
            "patch": "partial_update",
            "delete": "perform_destroy",
            "post": "perform_create",
            "get": "get_queryset"
        }

        if not check_viewset_methods(class_view_set, http_methods):
            raise ValueError(
                f"The provided {class_view_set.__name__} does not have"
                f" the required methods! Please check the provided viewset and"
                f" HTTP methods.")

        for http_method in http_methods:
            test_method = f"test_{http_methods_to_test[http_method]}"
            if not hasattr(cls, test_method):
                raise NotImplementedError(
                    f"{test_method} method is required for the"
                    f" '{http_method}' HTTP method.")

        return cls

    return decorator
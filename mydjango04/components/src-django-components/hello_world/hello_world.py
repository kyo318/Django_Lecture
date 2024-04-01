from django_components import component


@component.register("hello-world")
class HelloWorld(component.Component):
    template_name = "hello_world/hello_world.html"

    def get_context_data(self, name=None):
        return {"name": name}

    class Media:
        css = {"all": ["hello_world/hello_world.css"]}
        js = ["hello_world/hello_world.js"]

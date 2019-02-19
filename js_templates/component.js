var component__{{ component.name }} = function(element) {
    {% if not component.component %}
        var _this = this;
        _this.state = {};

        this.elements = {}
        {% for el in component.elements %}
           this.elements['{{el.get("element", "")}}'] = document.querySelector('*[fs-id="{{ component.hashname + "_" + el.get("element", "") }}"]');
        {% endfor %}
    {% endif %} 

    this.getElement = function(name) { return this.elements[name]; }

    if (!element)
        _this.element = document.querySelector('*[fs-id="{{ component.hashname }}"]');
    else _this.element = element;

    {{ component_body }}


    {% for el in component.get_component_elements() %}
        new window['component__{{ el.get("cname") }}'](document.querySelector('*[fs-id="{{ component.hashname }}"][fs-id-suffix="{{ loop.index-1 }}"]'));
    {% endfor %}
};
window.component__{{ component.name }} = component__{{ component.name }};

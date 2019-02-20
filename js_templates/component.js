var component__{{ component.name }} = function(element) {
    console.log('{{ component.name }}');
    {% if not component.component %}
        var _this = this;
        _this.state = {};

        // accessible elements
        this.elements = {}
        {% for el in component.elements %}
           {% if el.get('element') %}
               this.elements['{{el.get("element", "")}}'] = document.querySelector('*[fs-id="{{ component.hashname + "_" + el.get("element", "") }}"]');
           {% endif %}
        {% endfor %}
    {% endif %} 

    // helper functions
    this.getElement = function(name) { return this.elements[name]; }

    // make sure the component has an element
    if (!element)
        _this.element = document.querySelector('*[fs-id="{{ component.hashname }}"]');
    else _this.element = element;

    // component body
    {{ component_body }}

    {% for el in component.get_component_elements() %}
        new window['component__{{ el.get("cname") }}'](document.querySelector('*[fs-id="{{ component.hashname }}"][fs-id-suffix="{{ loop.index-1 }}"]'));
    {% endfor %}
};

// make sure the component is within the whole scope
window.component__{{ component.name }} = component__{{ component.name }};

// instantiate the root component
{% if not component.component and not component.abstract %}
    new component__{{ component.name }}();
{% endif %}

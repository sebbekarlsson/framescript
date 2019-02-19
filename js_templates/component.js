var component__{{ component.name }} = new function() {
    {% if not component.component %}
        var _this = this;
        _this.state = {};

        this.elements = {}
        {% for el in component.elements %}
           this.elements['{{el.name}}'] = document.querySelector('.{{ el.classname }}');
        {% endfor %}
    {% endif %} 

    this.getElement = function(name) { return this.elements[name]; }

    _this.element = document.getElementById('component__{{ component.name }}');

    {{ component_body }}
};

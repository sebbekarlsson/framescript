var component__{{ component.name }} = new function() {
    {% if not component.component %}
        var _this = this;
        _this.state = {};
    {% endif %}

    _this.element = document.getElementById('component__{{ component_name }}');

    {{ component_body }}
}

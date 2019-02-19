_this.element.addEventListener('{{event_name}}', function({{ variable_name }}) {
    var _old_state = JSON.parse(JSON.stringify(_this.state));
    {{ code }}
    var _new_state = _this.state;

    if (JSON.stringify(_old_state) != JSON.stringify(_new_state))
        _this.stateChanged(_new_state);
});

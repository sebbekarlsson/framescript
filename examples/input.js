component[base] {
    component[myinput] {
        style <%
            box-sizing: border-box;
            padding: 0.5rem;
            border-radius: 8px;
            font-size: 100%;
            font-family: Sans-Serif;
            font-weight: 600;
        %>;

        listen keyup as e <%
            me.state.text = e.target.value;
        %>;

        render <%
            <input/>
        %>;
    };

    component[view] {
        stateChanged as state <%
            me.getElement('text').innerHTML = state['text'];
        %>;

        render <%
            <div>
                <div element="text"></div>
            </div>
        %>;
    };

    render <%
        <div>
            <component cname="myinput"/>
            <component cname="view"/>
        </div>
    %>;
};

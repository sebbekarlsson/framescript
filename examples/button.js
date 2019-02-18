component[base] {
    constructor <%
        me.state['data'] = 0;
    %>;

    component[btn] { 
        listen click as e <%
            me.state['data'] = me.state['data'] + 1;
        %>;

        render <%
            <button>Update</button>
        %>;
    };

    render <%
        <div>
            <pre sync='data'></pre>
            <component name='btn'/>
        </div>
    %>;
};

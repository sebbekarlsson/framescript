component[base] {
    style <%
        background-color: rgb(48, 48, 48);
        color: white;
        font-family: Sans-Serif;
        display: inline-block;
        text-align: center;
    %>;

    constructor <%
        me.state['data'] = 0;
    %>;

    component[btn_increase] {
        listen click as e <%
            me.state['data'] = me.state['data'] + 1;
        %>;

        render <%
            <button>Increase</button>
        %>;
    };

    component[btn_decrease] {
        listen click as e <%
            me.state['data'] = me.state['data'] - 1;
        %>;

        render <%
            <button>Decrease</button>
        %>;
    };

    stateChanged as state <%
        me.getElement('data').innerHTML = state['data'];    
    %>;

    render <%
        <div>
            <pre element='data'></pre>
            <component cname='btn_decrease'/>
            <component cname='btn_increase'/>
        </div>
    %>;
};

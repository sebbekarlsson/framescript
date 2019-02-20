# Components Inside Components
> You can render components inside other components, using the `<component>`
> tag like this:
```elm
import "./myothercomponent.js";

component[mycomponent] {
    render <%
        <div>
            <h2>Hello!</h2>
            <component cname="myothercomponent"/>
        </div>
    %>;    
};
```
> The `myothercomponent` in this case, should probably be `abstract`,
> [Look here for more information](abstract_components.md)

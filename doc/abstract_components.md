# Abstract Components
> If you plan to write components that you will re-use as separate modules,
> then they should probably be abstract.  
> Abstract components only render if they have been initialized.

> You can create an abstract component by using the `abstract` keyword like
> this:
```elm
component[button] abstract {
    ...    
};
```
> This component will only render if it has been initialized using a
> `<component/>` tag, like this:
```elm
component[app] {
    render <%
        <component cname="button"/>
    %>;    
};
```

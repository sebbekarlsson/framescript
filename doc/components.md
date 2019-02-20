# Writing Components
> The basic structure looks like this:
```elm
component[<name>] {
    <body>    
};
```
> Example:
```elm
component[button] {
    render <%
        <button>Click Me</button>
    %>;    
};
```
> Now you have also been introduced to the `render` clause, let's talk about
> that...

## Render
> The `render` clause is where your markup goes and what will be seen in the
> browser.

## Event Listener
> There is also a `listen` clause that you can use to listen on events,
> the syntax looks like this:
```
listen <event_name> as <variable_name> <code>
```
> example:
```elm
component[button] {
    ...
    listen click as e <%
        console.log('I was clicked!');
    %>;
    ...    
};
```

## Me
> There is a mysterious `me` variable that you can use to access the most
> outer component (the parent of all components if you have a tree of components)

> This `me` variable is usually used to change the state, like this:
```elm
component[button] {
    listen click as e <%
        me.state['number_of_clicks'] = me.state['number_of_clicks'] + 1;
    %>;  
};
```

## stateChanged
> There is also a `stateChanged` clause that you can use to perform tasks
> when the state of the component is changed,
> The syntax for this is:
```
stateChanged as <variable_name>
```
> example:
```elm
component[board] {
    stateChanged as state <%
        me.getElement('title').innerHTML = state['title'];
    %>;
}
```

## getElement
> The `getElement(<element_name>)` method is used to access child-elements that the component
> might own.
> Example:
```elm
me.getElement('title').innerHTML = state['title'];
```

## Child Elements
> To make elements a "part" of the component and accessible with the
> `getElement` method, you have to specify that in the render method by
> setting `element` attributes on your elements, like this:
```elm
component[button] {
    render <%
        <button element="myAwesomeButton">Click Me</button>
    %>;    
};
```
> Now you can access this element by using `me.getElement("myAwesomeButton")`.

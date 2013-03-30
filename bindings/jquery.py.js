J = {};
parents = new Array();
var J____init__ = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
set_attribute(self, "j", jQuery(arg));
}

J.__init__ = J____init__;
var J__add = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.add(arg);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.add = J__add;
var J__addClass = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "klass")};
parameters = get_arguments(parameters, args, kwargs);
klass = parameters["klass"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.addClass(klass);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.addClass = J__addClass;
var J__after = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.after(arg);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.after = J__after;
var J__animate = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "properties", "duration", "easing", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
easing = parameters["easing"];
duration = parameters["duration"];
properties = parameters["properties"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.animate(properties, duration, easing, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.animate = J__animate;
var J__append = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.append(arg);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.append = J__append;
var J__appendTo = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.appendTo(arg);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.appendTo = J__appendTo;
var J__attr = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.attr(arg);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.attr = J__attr;
var J__before = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "arg")};
parameters = get_arguments(parameters, args, kwargs);
arg = parameters["arg"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.before(arg);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.before = J__before;
var J__bind = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "event_type", "event_data", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
event_data = parameters["event_data"];
event_type = parameters["event_type"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.bind(event_type, event_data, handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.bind = J__bind;
var J__blur = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.blur(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.blur = J__blur;
var J__change = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.change(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.change = J__change;
var J__children = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "selector")};
parameters = get_arguments(parameters, args, kwargs);
selector = parameters["selector"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.children(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.children = J__children;
var J__click = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.click(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.click = J__click;
var J__clone = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "with_data_and_events")};
parameters = get_arguments(parameters, args, kwargs);
with_data_and_events = parameters["with_data_and_events"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.clone(with_data_and_events);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.clone = J__clone;
var J__contents = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self")};
parameters = get_arguments(parameters, args, kwargs);
self = parameters["self"];
j = get_attribute(self, "j");
o = j.contents();
return get_attribute(J, "__call__")(new Array(o), {});
}

J.contents = J__contents;
var J__css = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "name", "value")};
parameters = get_arguments(parameters, args, kwargs);
value = parameters["value"];
name = parameters["name"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.css(name, value);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.css = J__css;
var J__data = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "key", "value")};
parameters = get_arguments(parameters, args, kwargs);
value = parameters["value"];
key = parameters["key"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.data(key, value);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.data = J__data;
var J__double_click = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.dbclick(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.double_click = J__double_click;
var J__delay = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "time", "queue_name")};
parameters = get_arguments(parameters, args, kwargs);
queue_name = parameters["queue_name"];
time = parameters["time"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.delay(time, queue_name);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.delay = J__delay;
var J__dequeue = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "queue_name")};
parameters = get_arguments(parameters, args, kwargs);
queue_name = parameters["queue_name"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.dequeue(queue_name);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.dequeue = J__dequeue;
var J__detach = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "selector")};
parameters = get_arguments(parameters, args, kwargs);
selector = parameters["selector"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.detach(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.detach = J__detach;
var J__each = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.each(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.each = J__each;
var J__end = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.end();
return get_attribute(J, "__call__")(new Array(o), {});
}

J.end = J__end;
var J__eq = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "index")};
parameters = get_arguments(parameters, args, kwargs);
index = parameters["index"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.eq(index);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.eq = J__eq;
var J__error = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.error(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.error = J__error;
var J__fade_in = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.fadeIn(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.fade_in = J__fade_in;
var J__fade_out = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.fadeOut(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.fade_out = J__fade_out;
var J__fadeTo = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "opacity", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
opacity = parameters["opacity"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.fade_to(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.fadeTo = J__fadeTo;
var J__fade_toggle = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "easing", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
easing = parameters["easing"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.fade_toggle(duration, easing, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.fade_toggle = J__fade_toggle;
var J__filter = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "selector")};
parameters = get_arguments(parameters, args, kwargs);
selector = parameters["selector"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.filter(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.filter = J__filter;
var J__finish = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "queue")};
parameters = get_arguments(parameters, args, kwargs);
queue = parameters["queue"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.finish(queue);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.finish = J__finish;
var J__first = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self")};
parameters = get_arguments(parameters, args, kwargs);
self = parameters["self"];
j = get_attribute(self, "j");
o = j.first();
return get_attribute(J, "__call__")(new Array(o), {});
}

J.first = J__first;
var J__focus = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.focus(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.focus = J__focus;
var J__focus_in = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.focusIn(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.focus_in = J__focus_in;
var J__focus_out = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.focusOut(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.focus_out = J__focus_out;
var J__get = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "index")};
parameters = get_arguments(parameters, args, kwargs);
index = parameters["index"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.get(index);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.get = J__get;
var J__has_class = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "name")};
parameters = get_arguments(parameters, args, kwargs);
name = parameters["name"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.has_class(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.has_class = J__has_class;
var J__height = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "value")};
parameters = get_arguments(parameters, args, kwargs);
value = parameters["value"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.height(value);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.height = J__height;
var J__hide = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.hide(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.hide = J__hide;
var J__hover = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.hover(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.hover = J__hover;
var J__html = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "value")};
parameters = get_arguments(parameters, args, kwargs);
value = parameters["value"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.html(value);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.html = J__html;
var J__index = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "selector")};
parameters = get_arguments(parameters, args, kwargs);
selector = parameters["selector"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.index(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.index = J__index;
var J__inner_height = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self")};
parameters = get_arguments(parameters, args, kwargs);
self = parameters["self"];
j = get_attribute(self, "j");
o = j.innerHeight();
return get_attribute(J, "__call__")(new Array(o), {});
}

J.inner_height = J__inner_height;
var J__inner_width = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self")};
parameters = get_arguments(parameters, args, kwargs);
self = parameters["self"];
j = get_attribute(self, "j");
o = j.innerWidth();
return get_attribute(J, "__call__")(new Array(o), {});
}

J.inner_width = J__inner_width;
var J__insert_after = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "target")};
parameters = get_arguments(parameters, args, kwargs);
target = parameters["target"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.insertAfter(target);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.insert_after = J__insert_after;
var J__insert_before = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "target")};
parameters = get_arguments(parameters, args, kwargs);
target = parameters["target"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.insertBefore(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.insert_before = J__insert_before;
var J__is_ = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "name")};
parameters = get_arguments(parameters, args, kwargs);
name = parameters["name"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.is(selector);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.is_ = J__is_;
var J__keydown = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.keydown(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.keydown = J__keydown;
var J__keypress = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.keypress(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.keypress = J__keypress;
var J__keyup = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.keyup(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.keyup = J__keyup;
var J__last = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.last(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.last = J__last;
var J__on = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "event", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
event = parameters["event"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.on(event, handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.on = J__on;
var J__load = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "url", "data", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
data = parameters["data"];
url = parameters["url"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.load(url, data, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.load = J__load;
var J__select = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.select(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.select = J__select;
var J__show = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.show(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.show = J__show;
var J__siblings = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "selector")};
parameters = get_arguments(parameters, args, kwargs);
selector = parameters["selector"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.select(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.siblings = J__siblings;
var J__size = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self")};
parameters = get_arguments(parameters, args, kwargs);
self = parameters["self"];
j = get_attribute(self, "j");
o = j.size();
return get_attribute(J, "__call__")(new Array(o), {});
}

J.size = J__size;
var J__slice = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "start", "end")};
parameters = get_arguments(parameters, args, kwargs);
end = parameters["end"];
start = parameters["start"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.slice(start, end);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.slice = J__slice;
var J__slide_down = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.slideDown(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.slide_down = J__slide_down;
var J__slide_toggle = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.slideToggle(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.slide_toggle = J__slide_toggle;
var J__slide_up = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.slideUp(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.slide_up = J__slide_up;
var J__stop = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "clear_queue", "jump_to_end")};
parameters = get_arguments(parameters, args, kwargs);
jump_to_end = parameters["jump_to_end"];
clear_queue = parameters["clear_queue"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.stop(clear_queue, jump_to_end);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.stop = J__stop;
var J__submit = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "clear_queue", "jump_to_end")};
parameters = get_arguments(parameters, args, kwargs);
jump_to_end = parameters["jump_to_end"];
clear_queue = parameters["clear_queue"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.submit(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.submit = J__submit;
var J__text = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "text")};
parameters = get_arguments(parameters, args, kwargs);
text = parameters["text"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.text(text);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.text = J__text;
var J__toggle = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "duration", "complete")};
parameters = get_arguments(parameters, args, kwargs);
complete = parameters["complete"];
duration = parameters["duration"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.toggle(duration, complete);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.toggle = J__toggle;
var J__toggle_class = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "class_name")};
parameters = get_arguments(parameters, args, kwargs);
class_name = parameters["class_name"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.toggleClass(class_name);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.toggle_class = J__toggle_class;
var J__trigger = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "event")};
parameters = get_arguments(parameters, args, kwargs);
event = parameters["event"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.trigger(event);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.trigger = J__trigger;
var J__unbind = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "event", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
event = parameters["event"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.unbind(event, handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.unbind = J__unbind;
var J__value = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "value")};
parameters = get_arguments(parameters, args, kwargs);
value = parameters["value"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.val(value);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.value = J__value;
var J__width = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "value")};
parameters = get_arguments(parameters, args, kwargs);
value = parameters["value"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.width(value);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.width = J__width;
var J__length = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self")};
parameters = get_arguments(parameters, args, kwargs);
self = parameters["self"];
j = get_attribute(self, "j");
return j.length();
}

J.length = J__length;
var J__map = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "func")};
parameters = get_arguments(parameters, args, kwargs);
func = parameters["func"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.map(func);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.map = J__map;
var J__mousedown = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mousedown(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mousedown = J__mousedown;
var J__mouseenter = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mouseenter(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mouseenter = J__mouseenter;
var J__mouseleave = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mouseleave(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mouseleave = J__mouseleave;
var J__mousemove = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mousemove(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mousemove = J__mousemove;
var J__mouseout = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mouseout(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mouseout = J__mouseout;
var J__mouseover = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mouseover(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mouseover = J__mouseover;
var J__mouseup = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("self", "handler")};
parameters = get_arguments(parameters, args, kwargs);
handler = parameters["handler"];
self = parameters["self"];
j = get_attribute(self, "j");
o = j.mouseup(handler);
return get_attribute(J, "__call__")(new Array(o), {});
}

J.mouseup = J__mouseup;
J = create_class("J", parents, J);
var ajax = function(args, kwargs) {
parameters = {"kwargs": {}, "args": new Array("url", "settings")};
parameters = get_arguments(parameters, args, kwargs);
settings = parameters["settings"];
url = parameters["url"];
return jQuery.ajax(url, settings);
}


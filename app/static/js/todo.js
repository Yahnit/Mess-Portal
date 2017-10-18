var makeTodo = function (todoData) {
    var data = {
        title: todoData.title,
        text: todoData.text,
        done: todoData.done,
        color: todoData.color,
    };
    var getData = function () {
        return data;
    };
    var t = {};
    t.getData = getData;
    return t;
};

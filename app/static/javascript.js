$(document).ready(function(){
    jQuery.fn.center = function () {
        this.css("position","absolute");
        this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) +
                                                    $(window).scrollTop()) + "px");
        this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +
                                                    $(window).scrollLeft()) + "px");
        return this;
    }
    String.prototype.replaceAll = function(search, replacement) {
        var target = this;
        return target.split(search).join(replacement);
    };

    function PosLine(id) {
        function PosInfo(id) {
            var info = $('#info_' + id);
            var width = $('.container-1__inner > .new').width();
            info.width(width);
            info.height(width);
            info.css('top', -width/2);
        }
        var line = $('#line_' + id);
        var stack = $('#stack_' + id);
        var container = $('.container-2');
        var x1 = stack.offset().left + stack.width();
        var y1 = stack.offset().top + stack.height() / 2;
        var x2 = container.offset().left;
        var y2 = container.offset().top + container.height() / 2;
        var angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
        var distance = Math.sqrt((x2-x1) * (x2-x1) + (y2-y1)*(y2-y1));
        // Set Angle
        $(line).css('transform', 'rotate(' + angle + 'deg)');
        // Set Width
        $(line).css('width', distance + 'px');
        // Set Position

        if(y2 < y1) {
            $(line).offset({top: y2, left: x1});
        } else {
            $(line).offset({top: y1, left: x1});
        }
        PosInfo(id);

    }

    function PosLines() {
        var lines = $('.line');
        lines.each(function(index) {
            PosLine(index);
        });
    }

    function ChangeText(proba) {
        var elems = $('.info');
        elems.children('p').text(function(index) {
            return proba[index];
        });
    }

    function CorrectScale() {
        $('.container-1__inner').height($('.container-2').width());
        $('.new').height($('.container-2').width() * 0.8);
        $('.new').width($('.container-2').width() * 0.8);
        PosLine(0);
    }
    CorrectScale();
    var n_neighbors = 5;

    function ChangeNeighbors(n) {
        if(n_neighbors != 'all') {
            n_neighbors = parseFloat(n);
        }
    }

    $(document).on("submit", '#change_form', function() {
        var form_data = $('#change_form').serialize();
        $.get(
            '/change',
            form_data,
            function(data) {
                if(data.error) {
                    alert(data.error);
                }
                else {
                    ChangeNeighbors(data.n_neighbors);
                }
            }
        )
    });

    $(document).on({
        mouseenter: function() {
            $(this).css('z-index', 10000);
        },
        mouseleave: function() {
            var ind = $('.container-1__inner > .new').index($(this));
            $(this).css('z-index', ind);
        }
    }, '.container-1__inner > .new');


    function AlertData(data) {
        var elem = $(data)
        elem.appendTo('body').draggable();
        elem.center();
    }

    $(document).on(
        'click',
        '.new:not(#empty)',
        function(ev) {
            $.get(
                '/js',
                {key_code: 'click', id: $(this).attr('id')},
                function(data) {
                    AlertData(data);
                }
            )
        }
    )

    $(document).on(
        'click',
        '.modal__close',
        function(ev) {
            $(this).parent('.modal').remove();
        }
    )


    function CorrectStack(stack) {
        var stack = $('#stack_' + stack);
        var len = stack.children().length;

        stack.children().css('left', function(index, value) {
            var new_left = index * stack.height();
            return new_left;
        })

        if(stack.height() * len > stack.width()) {
            var diff = stack.height() * len - stack.width();

            stack.children().css('left', function(index, value) {
                var new_left = parseInt(value.replace('px', '')) - diff / len * index;
                return new_left;
            })
        }

        $('.container-1__inner > .new').css('z-index', function(index, value) {
            return index;
        })
    }

    function CorrectStacks() {
        var stacks = $('.container-1__inner');

        stacks.each(function(index) {
            CorrectStack(index);
        });
    }
    function CorrectLeftScale() {
        $('.container-1__inner').height($('.container-1__inner').height());
        $('.container-1__inner > .new').height($('.container-1__inner').height() * 0.8);
        $('.container-1__inner > .new').width($('.container-1__inner').height() * 0.8);
    }
    function CorrectRightScale() {
        $('.container-2 > .new').width($('.container-2').width());
        $('.container-2 > .new').height($('.container-2').width());
    }
    function AnimateLine(line, direction) {
        var color;
        if(direction == 'to') {color = 'rgba(0, 255, 0'}
        else if(direction == 'from') {color = 'rgba(225, 0, 0'}
        else {return};

        var old_background = line.css('background');
        var new_background = old_background
            .replaceAll('rgba(0, 0, 0, 0)', color + ', 0.5)')
            .replaceAll('rgb(0, 0, 0)', color + ')');
        var old_height = line.height();
        var new_height = old_height * 2;
        line.animate({ HelloWorld: 69}, {
            step: function(now,fx) {
                $(this).css('background', new_background);
                $(this).height(new_height);
            },
            duration: 100,
        }, 'linear', function() {
        });
        line.animate({ HelloWorld: 69 }, {
            step: function(now,fx) {
                $(this).css('background', old_background);
                $(this).height(old_height);

            },
            duration: 100,
        }, 'linear', function() {

        });
        //line.css('background', old_background);
    }

    function FlyTo(n, time) {
        function AppendNew(elem) {
            $('#stack_' + n).append(elem);
        }
        var flag = false;
        var first = $('.container-2 > .new').first();

        if(parseInt(n) >= $('.container-1__inner').length - 1) {
            $('.container-1').append('<div class="container-1__inner" id="stack_' + (parseInt(n) + 1) + '"></div>');
            $('.canvas').append('<div class="line" id="line_' +
                (parseInt(n) + 1) +
                '"> <div class="info" id="info_' +
                (parseInt(n) + 1) +
                '"><p></p></div> </div>');
            $('#stack_' + (parseInt(n) + 1)).append($('#empty'));

            flag = true;
        }

        AppendNew(first);
        if(flag){AnimateLine($('#line_' + (parseInt(n) + 1)), 'to');}
        else {AnimateLine($('#line_' + n), 'to')};
        return flag;
    }

    function FlyFrom(n) {
        function PopNew(elem) {
            elem.appendTo($('.container-2'));
            elem.css('left', 0);
        }
        var flag = false;
        var first = $('.container-2 > .new').first();
        var elem = $('#stack_' + n).children().last();
        PopNew(elem);
        first.remove();
        if($('#stack_' + n).children().length == 0) {
            $('#stack_' + n).remove();
            $('.container-1__inner').last().attr('id', 'stack_' + n);
            $('.line').last().remove();
            flag = true;
        }
        AnimateLine($('#line_' + n), 'from');
        return flag;
    }


    var max_size = 1;
    var height_stack = [$('.container-1__inner').height()];
    var curr_stack = 0;
    var stack_n_neighbors = [1];

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    function PushBack(stack, n) {
        var stack = $('#stack_' + stack);
        stack.children().slice(0,n).remove();
    }

    $(document).keypress(function(ev) {
        if(ev.which == 100 || ev.which == 97) {
            $.get(
                '/js', {
                    key_code: ev.which
                }, async function(data) {


                    if(data.event == 'add') {
                        $('.container-2').append("<div class='new' id='" + data.id + "'></div>");
                        CorrectRightScale();
                        //alert(stack_n_neighbors);
                        var time = 0;
                        var proba = data.proba.split(' ').map(function(currentValue, index) {
                            return parseFloat(currentValue).toFixed(2);
                        });
                        var flag = FlyTo(curr_stack, 0);
                        //await sleep(time + 10);


                        if($('#stack_' + curr_stack).children().length > stack_n_neighbors[curr_stack]) {
                            $('#stack_' + curr_stack).children().first().remove();
                        }

                        CorrectLeftScale();
                        CorrectStack(curr_stack);
                        if(flag) {
                            CorrectStacks();
                            PosLines(proba);
                            height_stack.push($('.container-1__inner').height());
                        }
                        stack_n_neighbors[data.stack] = parseInt(data.n_neighbors);

                        ChangeText(proba);
                        curr_stack = data.stack;

                    }
                    else if(data.event == 'sub') {
                        var stack = $('#stack_' + data.stack);
                        var proba = data.proba.split(' ').map(function(currentValue, index) {
                            return parseFloat(currentValue).toFixed(2);
                        });
                        CorrectRightScale();

                        if(data.n_neighbors < stack.children().length){
                            PushBack(data.stack, 1);
                        }
                        if(data.id != 'nothing') {
                            $('#stack_' + data.stack).prepend("<div class='new' id='" + data.id + "'></div>");
                        }

                        var flag = FlyFrom(data.stack);

                        CorrectLeftScale();
                        CorrectStack(data.stack);
                        if (flag) {
                            height_stack.pop();
                            var height = height_stack[height_stack.length - 1];
                            $('.container-1__inner').height(height);
                            CorrectStacks();
                            PosLines();
                        }

                        ChangeText(proba);
                    }

                    else {
                    }
            });
        }
    });
});
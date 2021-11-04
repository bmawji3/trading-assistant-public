/* Theme Name: Tradify - Responsive Crypto/Stock Trading User Interface
   Author: CoderBoys
   Version: 1.0.0
   Created:April 2018
   File Description: Powerful Stock & Crypto Trading User interface
*/

"use strict"; 

! function(e, t, o) {
    var a = '[data-toggle="aside"]',
        n = e("body");
    e(o).on("click", a, function(e) {
        e.preventDefault(), n.toggleClass("aside-toggled")
    })
}(jQuery, window, document),
function(e, t, o) {
    function a(t, o) {
        var a = e("#remove-after-drop");
        t.fullCalendar({
            header: {
                left: "prev,next today",
                center: "title",
                right: "month,agendaWeek,agendaDay"
            },
            buttonIcons: {
                prev: " fa fa-caret-left",
                next: " fa fa-caret-right"
            },
            buttonText: {
                today: "today",
                month: "month",
                week: "week",
                day: "day"
            },
            editable: !0,
            droppable: !0,
            drop: function(o, n) {
                var r = e(this),
                    i = r.data("calendarEventObject");
                if (i) {
                    var s = e.extend({}, i);
                    s.start = o, s.allDay = n, s.backgroundColor = r.css("background-color"), s.borderColor = r.css("border-color"), t.fullCalendar("renderEvent", s, !0), a.is(":checked") && r.remove()
                }
            },
            eventDragStart: function(e, t, o) {
                draggingEvent = e
            },
            events: o
        })
    }

    function n(t) {
        var o = e(".external-events");
        new i(o.children("div"));
        var a = "#f6504d",
            n = e(".external-event-add-btn"),
            r = e(".external-event-name"),
            s = e(".external-event-color-selector .point");
        e(".external-events-trash").droppable({
            accept: ".fc-event",
            activeClass: "active",
            hoverClass: "hovered",
            tolerance: "touch",
            drop: function(e, o) {
                if (draggingEvent) {
                    var a = draggingEvent.id || draggingEvent._id;
                    t.fullCalendar("removeEvents", a), o.draggable.remove(), draggingEvent = null
                }
            }
        }), s.click(function(t) {
            t.preventDefault();
            var o = e(this);
            a = o.css("background-color"), s.removeClass("selected"), o.addClass("selected")
        }), n.click(function(t) {
            t.preventDefault();
            var n = r.val();
            if ("" !== e.trim(n)) {
                var s = e("<div/>").css({
                    "background-color": a,
                    "border-color": a,
                    color: "#fff"
                }).html(n);
                o.prepend(s), new i(s), r.val("")
            }
        })
    }

    function r() {
        var e = new Date,
            t = e.getDate(),
            o = e.getMonth(),
            a = e.getFullYear();
        return [{
            title: "All Day Event",
            start: new Date(a, o, 1),
            backgroundColor: "#f56954",
            borderColor: "#f56954"
        }, {
            title: "Long Event",
            start: new Date(a, o, t - 5),
            end: new Date(a, o, t - 2),
            backgroundColor: "#f39c12",
            borderColor: "#f39c12"
        }, {
            title: "Meeting",
            start: new Date(a, o, t, 10, 30),
            allDay: !1,
            backgroundColor: "#0073b7",
            borderColor: "#0073b7"
        }, {
            title: "Lunch",
            start: new Date(a, o, t, 12, 0),
            end: new Date(a, o, t, 14, 0),
            allDay: !1,
            backgroundColor: "#00c0ef",
            borderColor: "#00c0ef"
        }, {
            title: "Birthday Party",
            start: new Date(a, o, t + 1, 19, 0),
            end: new Date(a, o, t + 1, 22, 30),
            allDay: !1,
            backgroundColor: "#00a65a",
            borderColor: "#00a65a"
        }, {
            title: "Open Google",
            start: new Date(a, o, 28),
            end: new Date(a, o, 29),
            url: "http://google.com/",
            backgroundColor: "#3c8dbc",
            borderColor: "#3c8dbc"
        }]
    }
    if (e.fn.fullCalendar) {
        var i = function(t) {
            t && t.each(function() {
                var t = e(this),
                    o = {
                        title: e.trim(t.text())
                    };
                t.data("calendarEventObject", o), t.draggable({
                    zIndex: 1070,
                    revert: !0,
                    revertDuration: 0
                })
            })
        };
        e(function() {
            var t = e("#calendar"),
                o = r();
            n(t), a(t, o)
        })
    }
}(jQuery, window, document),
function(e, t, o) {
    e(function() {
        if (e.fn.dataTable) {
            e("#datatable1").dataTable({
                paging: !0,
                ordering: !0,
                info: !0,
                oLanguage: {
                    sSearch: "Search:",
                    sLengthMenu: "_MENU_",
                    info: "Showing page _PAGE_ of _PAGES_",
                    zeroRecords: "Nothing found - sorry",
                    infoEmpty: "No records available",
                    infoFiltered: "(filtered from _MAX_ total records)"
                }
            });
            var t = e("#datatable2").dataTable({
                    paging: !0,
                    ordering: !0,
                    info: !0,
                    oLanguage: {
                        sSearch: "Search:",
                        sLengthMenu: "_MENU_",
                        info: "Showing page _PAGE_ of _PAGES_",
                        zeroRecords: "Nothing found - sorry",
                        infoEmpty: "No records available",
                        infoFiltered: "(filtered from _MAX_ total records)"
                    }
                }),
                o = "datatable_input_col_search",
                a = e("tfoot ." + o);
            a.keyup(function() {
                t.fnFilter(this.value, a.index(this))
            });
            var table = e("#datatable3").dataTable({
                paging: !0,
                ordering: !0,
                info: !0,
                oLanguage: {
                    sSearch: "Search:",
                    sLengthMenu: "_MENU_",
                    info: "Showing page _PAGE_ of _PAGES_",
                    zeroRecords: "Nothing found - sorry",
                    infoEmpty: "No records available",
                    infoFiltered: "(filtered from _MAX_ total records)"
                }
            })
            e('.toggle-vis').on('click', function() {
                e(this).toggleClass('btn-info');
                var iCol = e(this).attr('data-col');
                var oTable = e('#datatable3').dataTable();
                var bVis = oTable.fnSettings().aoColumns[iCol].bVisible;
                oTable.fnSetColumnVis(iCol, bVis ? false : true);
            });
        }
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = ".datetimepicker";
    e(a).each(function() {
        var t = e(this),
            a = t.data();
        t.datetimepicker(e.extend(a, {
            icons: {
                time: "fa fa-clock-o",
                date: "fa fa-calendar",
                up: "fa fa-arrow-up",
                down: "fa fa-arrow-down"
            }
        })), e(o).on("click", function() {
            t.data("DateTimePicker").hide()
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    e(function() {
        var t = ".dropdown-toggle[data-play]",
            o = e(t).parent();
        o.on("show.bs.dropdown", function(t) {
            var o = e(this),
                a = o.children(".dropdown-toggle"),
                n = a.data("play"),
                r = a.data("duration") || .5,
                i = o.children(".dropdown-menu");
            i && i.length ? e.fn.animo && n && i.animo({
                animation: n,
                duration: r
            }) : e.error("No target for play-animation")
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    t.FlotChart = function(t, o) {
        this.element = e(t), this.url = o, this.requestData = function(t, o, a) {
            var n = this;
            return a = o && e.isFunction(o) ? o : a, o = o && "string" == typeof o ? o : "POST", n.option = t, e.ajax({
                url: n.url,
                cache: !1,
                type: o,
                dataType: "json"
            }).done(function(o) {
                e.plot(n.element, o, t), a && a()
            }), this
        }, this.listen = function() {
            var e = this,
                t = this.element.parents(".panel").eq(0);
            return t.on("panel-refresh", function(t, o) {
                e.requestData(e.option, function() {
                    o.removeSpinner()
                })
            }), this
        }
    }, e(function() {
        ! function() {
            var t = ".chart-bar";
            e(t).each(function() {
                var o = e(this).data("source") || e.error("Bar: No source defined."),
                    a = new FlotChart(this, o),
                    n = (e(t).parents(".panel"), {
                        series: {
                            bars: {
                                align: "center",
                                lineWidth: 0,
                                show: !0,
                                barWidth: .6,
                                fill: .9
                            }
                        },
                        grid: {
                            borderColor: "#eee",
                            borderWidth: 1,
                            hoverable: !0,
                            backgroundColor: "#fcfcfc"
                        },
                        tooltip: !0,
                        tooltipOpts: {
                            content: "%x : %y"
                        },
                        xaxis: {
                            tickColor: "#fcfcfc",
                            mode: "categories"
                        },
                        yaxis: {
                            tickColor: "#eee"
                        },
                        shadowSize: 0
                    });
                a.requestData(n)
            })
        }(),
        function() {
            var t = ".chart-bar-stacked";
            e(t).each(function() {
                var t = e(this).data("source") || e.error("Bar Stacked: No source defined."),
                    o = new FlotChart(this, t),
                    a = {
                        series: {
                            stack: !0,
                            bars: {
                                align: "center",
                                lineWidth: 0,
                                show: !0,
                                barWidth: .6,
                                fill: .9
                            }
                        },
                        grid: {
                            borderColor: "#eee",
                            borderWidth: 1,
                            hoverable: !0,
                            backgroundColor: "#fcfcfc"
                        },
                        tooltip: !0,
                        tooltipOpts: {
                            content: "%x : %y"
                        },
                        xaxis: {
                            tickColor: "#fcfcfc",
                            mode: "categories"
                        },
                        yaxis: {
                            tickColor: "#eee"
                        },
                        shadowSize: 0
                    };
                o.requestData(a)
            })
        }(),
        function() {
            var t = ".chart-area";
            e(t).each(function() {
                var t = e(this).data("source") || e.error("Area: No source defined."),
                    o = new FlotChart(this, t),
                    a = {
                        series: {
                            lines: {
                                show: !0,
                                fill: .8
                            },
                            points: {
                                show: !0,
                                radius: 4
                            }
                        },
                        grid: {
                            borderColor: "#eee",
                            borderWidth: 1,
                            hoverable: !0,
                            backgroundColor: "#fcfcfc"
                        },
                        tooltip: !0,
                        tooltipOpts: {
                            content: "%x : %y"
                        },
                        xaxis: {
                            tickColor: "#fcfcfc",
                            mode: "categories"
                        },
                        yaxis: {
                            tickColor: "#eee",
                            tickFormatter: function(e) {
                                return e + " visitors"
                            }
                        },
                        shadowSize: 0
                    };
                o.requestData(a).listen()
            })
        }(),
        function() {
            var t = ".chart-line";
            e(t).each(function() {
                var t = e(this).data("source") || e.error("Line: No source defined."),
                    o = new FlotChart(this, t),
                    a = {
                        series: {
                            lines: {
                                show: !0,
                                fill: .01
                            },
                            points: {
                                show: !0,
                                radius: 4
                            }
                        },
                        grid: {
                            borderColor: "#eee",
                            borderWidth: 1,
                            hoverable: !0,
                            backgroundColor: "#fcfcfc"
                        },
                        tooltip: !0,
                        tooltipOpts: {
                            content: "%x : %y"
                        },
                        xaxis: {
                            tickColor: "#eee",
                            mode: "categories"
                        },
                        yaxis: {
                            tickColor: "#eee"
                        },
                        shadowSize: 0
                    };
                o.requestData(a)
            })
        }(),
        function() {
            var t = ".chart-pie";
            e(t).each(function() {
                var t = e(this).data("source") || e.error("Pie: No source defined."),
                    o = new FlotChart(this, t),
                    a = {
                        series: {
                            pie: {
                                show: !0,
                                innerRadius: 0,
                                label: {
                                    show: !0,
                                    radius: .8,
                                    formatter: function(e, t) {
                                        return '<div class="flot-pie-label">' + Math.round(t.percent) + "%</div>"
                                    },
                                    background: {
                                        opacity: .8,
                                        color: "#222"
                                    }
                                }
                            }
                        }
                    };
                o.requestData(a)
            })
        }(),
        function() {
            var t = ".chart-donut";
            e(t).each(function() {
                var t = e(this).data("source") || e.error("Donut: No source defined."),
                    o = new FlotChart(this, t),
                    a = {
                        series: {
                            pie: {
                                show: !0,
                                innerRadius: .5
                            }
                        }
                    };
                o.requestData(a)
            })
        }()
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = [{
            featureType: "water",
            stylers: [{
                visibility: "on"
            }, {
                color: "#bdd1f9"
            }]
        }, {
            featureType: "all",
            elementType: "labels.text.fill",
            stylers: [{
                color: "#334165"
            }]
        }, {
            featureType: "landscape",
            stylers: [{
                color: "#e9ebf1"
            }]
        }, {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{
                color: "#c5c6c6"
            }]
        }, {
            featureType: "road.arterial",
            elementType: "geometry",
            stylers: [{
                color: "#fff"
            }]
        }, {
            featureType: "road.local",
            elementType: "geometry",
            stylers: [{
                color: "#fff"
            }]
        }, {
            featureType: "transit",
            elementType: "geometry",
            stylers: [{
                color: "#d8dbe0"
            }]
        }, {
            featureType: "poi",
            elementType: "geometry",
            stylers: [{
                color: "#cfd5e0"
            }]
        }, {
            featureType: "administrative",
            stylers: [{
                visibility: "on"
            }, {
                lightness: 33
            }]
        }, {
            featureType: "poi.park",
            elementType: "labels",
            stylers: [{
                visibility: "on"
            }, {
                lightness: 20
            }]
        }, {
            featureType: "road",
            stylers: [{
                color: "#d8dbe0",
                lightness: 20
            }]
        }],
        n = '[data-toggle="gmap"]';
    if (e.fn.gMap) {
        var r = [];
        e(n).each(function() {
            var t = e(this),
                o = t.data("address") && t.data("address").split(";"),
                n = t.data("title") && t.data("title").split(";"),
                i = t.data("zoom") || 14,
                s = t.data("maptype") || "ROADMAP",
                l = [];
            if (o) {
                for (var d in o) "string" == typeof o[d] && l.push({
                    address: o[d],
                    html: n && n[d] || "",
                    popup: !0
                });
                var c = {
                        controls: {
                            panControl: !0,
                            zoomControl: !0,
                            mapTypeControl: !0,
                            scaleControl: !0,
                            streetViewControl: !0,
                            overviewMapControl: !0
                        },
                        scrollwheel: !1,
                        maptype: s,
                        markers: l,
                        zoom: i
                    },
                    u = t.gMap(c),
                    f = u.data("gMap.reference");
                r.push(f), void 0 !== t.data("styled") && f.setOptions({
                    styles: a
                })
            }
        })
    }
    e(t).resize(function() {
        if (r && r.length)
            for (var e in r) {
                var t = r[e],
                    o = t.getCenter();
                t && o && (google.maps.event.trigger(t, "resize"), t.setCenter(o))
            }
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = function(t, o) {
        var n = e(t);
        n.data("markdownarea") || (this.element = n, this.options = e.extend({}, a.defaults, o), this.marked = this.options.marked || marked, this.CodeMirror = this.options.CodeMirror || CodeMirror, this.marked.setOptions({
            gfm: !0,
            tables: !0,
            breaks: !0,
            pedantic: !0,
            sanitize: !1,
            smartLists: !0,
            smartypants: !1,
            langPrefix: "lang-"
        }), this.init(), this.element.data("markdownarea", this))
    };
    e.extend(a.prototype, {
        init: function() {
            var o = this,
                n = a.template;
            n = n.replace(/\{\:lblPreview\}/g, this.options.lblPreview), n = n.replace(/\{\:lblCodeview\}/g, this.options.lblCodeview), this.markdownarea = e(n), this.content = this.markdownarea.find(".uk-markdownarea-content"), this.toolbar = this.markdownarea.find(".uk-markdownarea-toolbar"), this.preview = this.markdownarea.find(".uk-markdownarea-preview").children().eq(0), this.code = this.markdownarea.find(".uk-markdownarea-code"), this.element.before(this.markdownarea).appendTo(this.code), this.editor = this.CodeMirror.fromTextArea(this.element[0], this.options.codemirror), this.editor.markdownarea = this, this.editor.on("change", function() {
                var t = function() {
                    var e = o.editor.getValue();
                    o.currentvalue = String(e), o.element.trigger("markdownarea-before", [o]), o.applyPlugins(), o.marked(o.currentvalue, function(e, t) {
                        if (e) throw e;
                        o.preview.html(t), o.element.val(o.editor.getValue()).trigger("markdownarea-update", [o])
                    })
                };
                return t(), e.Utils.debounce(t, 150)
            }()), this.code.find(".CodeMirror").css("height", this.options.height), this._buildtoolbar(), this.fit(), e(t).on("resize", e.Utils.debounce(function() {
                o.fit()
            }, 200));
            var r = o.preview.parent(),
                i = this.code.find(".CodeMirror-sizer"),
                s = this.code.find(".CodeMirror-scroll").on("scroll", e.Utils.debounce(function() {
                    if ("tab" != o.markdownarea.attr("data-mode")) {
                        var e = i.height() - s.height(),
                            t = r[0].scrollHeight - r.height(),
                            a = t / e,
                            n = s.scrollTop() * a;
                        r.scrollTop(n)
                    }
                }, 10));
            this.markdownarea.on("click", ".uk-markdown-button-markdown, .uk-markdown-button-preview", function(t) {
                t.preventDefault(), "tab" == o.markdownarea.attr("data-mode") && (o.markdownarea.find(".uk-markdown-button-markdown, .uk-markdown-button-preview").removeClass("uk-active").filter(this).addClass("uk-active"), o.activetab = e(this).hasClass("uk-markdown-button-markdown") ? "code" : "preview", o.markdownarea.attr("data-active-tab", o.activetab))
            }), this.preview.parent().css("height", this.code.height())
        },
        applyPlugins: function() {
            var e = this,
                t = Object.keys(a.plugins),
                o = a.plugins;
            if (this.markers = {}, t.length) {
                var n = this.currentvalue.split("\n");
                t.forEach(function(e) {
                    this.markers[e] = []
                }, this);
                for (var r = 0, i = n.length; i > r; r++) ! function(a) {
                    t.forEach(function(t) {
                        var r = 0;
                        n[a] = n[a].replace(o[t].identifier, function() {
                            var n = o[t].cb({
                                area: e,
                                found: arguments,
                                line: a,
                                pos: r++,
                                uid: [t, a, r, (new Date).getTime() + "RAND" + Math.ceil(1e5 * Math.random())].join("-"),
                                replace: function(e) {
                                    var t = this.area.editor.getLine(this.line),
                                        o = t.indexOf(this.found[0]);
                                    end = o + this.found[0].length, this.area.editor.replaceRange(e, {
                                        line: this.line,
                                        ch: o
                                    }, {
                                        line: this.line,
                                        ch: end
                                    })
                                }
                            });
                            return n
                        })
                    })
                }(r);
                this.currentvalue = n.join("\n")
            }
        },
        _buildtoolbar: function() {
            if (this.options.toolbar && this.options.toolbar.length) {
                var t = this,
                    o = [];
                this.options.toolbar.forEach(function(e) {
                    if (a.commands[e]) {
                        var n = a.commands[e].title ? a.commands[e].title : e;
                        o.push('<li><a data-markdownarea-cmd="' + e + '" title="' + n + '" data-toggle="tooltip">' + a.commands[e].label + "</a></li>"), a.commands[e].shortcut && t.registerShortcut(a.commands[e].shortcut, a.commands[e].action)
                    }
                }), this.toolbar.html(o.join("\n")), this.markdownarea.on("click", "a[data-markdownarea-cmd]", function() {
                    var o = e(this).data("markdownareaCmd");
                    !o || !a.commands[o] || t.activetab && "code" != t.activetab && "fullscreen" != o || a.commands[o].action.apply(t, [t.editor])
                })
            }
        },
        fit: function() {
            var e = this.options.mode;
            "split" == e && this.markdownarea.width() < this.options.maxsplitsize && (e = "tab"), "tab" == e && (this.activetab || (this.activetab = "code", this.markdownarea.attr("data-active-tab", this.activetab)), this.markdownarea.find(".uk-markdown-button-markdown, .uk-markdown-button-preview").removeClass("uk-active").filter("code" == this.activetab ? ".uk-markdown-button-markdown" : ".uk-markdown-button-preview").addClass("uk-active")), this.editor.refresh(), this.preview.parent().css("height", this.code.height()), this.markdownarea.attr("data-mode", e)
        },
        registerShortcut: function(t, o) {
            var a = this;
            t = e.isArray(t) ? t : [t];
            for (var n = 0, r = t.length; r > n; n++) {
                var i = {};
                i[t[n]] = function() {
                    o.apply(a, [a.editor])
                }, a.editor.addKeyMap(i)
            }
        },
        getMode: function() {
            var e = this.editor.getDoc().getCursor();
            return this.editor.getTokenAt(e).state.base.htmlState ? "html" : "markdown"
        }
    }), e.fn.markdownarea = function(t) {
        return this.each(function() {
            var o = e(this);
            if (!o.data("markdownarea")) {
                new a(o, t)
            }
        })
    };
    var n = function(e, t) {
        var o = t.getSelection(),
            a = e.replace("$1", o);
        t.replaceSelection(a, "end")
    };
    return a.commands = {
        fullscreen: {
            title: "Fullscreen",
            label: '<i class="fa fa-expand"></i>',
            action: function(a) {
                a.markdownarea.markdownarea.toggleClass("uk-markdownarea-fullscreen"), e("html").toggleClass("markdownarea-fullscreen"), e("html, body").scrollTop(0);
                var n = a.getWrapperElement();
                if (a.markdownarea.markdownarea.hasClass("uk-markdownarea-fullscreen")) a.state.fullScreenRestore = {
                    scrollTop: t.pageYOffset,
                    scrollLeft: t.pageXOffset,
                    width: n.style.width,
                    height: n.style.height
                }, n.style.width = "", n.style.height = a.markdownarea.content.height() + "px", o.documentElement.style.overflow = "hidden";
                else {
                    o.documentElement.style.overflow = "";
                    var r = a.state.fullScreenRestore;
                    n.style.width = r.width, n.style.height = r.height, t.scrollTo(r.scrollLeft, r.scrollTop)
                }
                a.refresh(), a.markdownarea.preview.parent().css("height", a.markdownarea.code.height())
            }
        },
        bold: {
            title: "Bold",
            label: '<i class="fa fa-bold"></i>',
            shortcut: ["Ctrl-B", "Cmd-B"],
            action: function(e) {
                n("html" == this.getMode() ? "<strong>$1</strong>" : "**$1**", e)
            }
        },
        italic: {
            title: "Italic",
            label: '<i class="fa fa-italic"></i>',
            action: function(e) {
                n("html" == this.getMode() ? "<em>$1</em>" : "*$1*", e)
            }
        },
        strike: {
            title: "Strikethrough",
            label: '<i class="fa fa-strikethrough"></i>',
            action: function(e) {
                n("html" == this.getMode() ? "<del>$1</del>" : "~~$1~~", e)
            }
        },
        blockquote: {
            title: "Blockquote",
            label: '<i class="fa fa-quote-right"></i>',
            action: function(e) {
                n("html" == this.getMode() ? "<blockquote><p>$1</p></blockquote>" : "> $1", e)
            }
        },
        link: {
            title: "Link",
            label: '<i class="fa fa-link"></i>',
            action: function(e) {
                n("html" == this.getMode() ? '<a href="http://">$1</a>' : "[$1](http://)", e)
            }
        },
        picture: {
            title: "Picture",
            label: '<i class="fa fa-picture-o"></i>',
            action: function(e) {
                n("html" == this.getMode() ? '<img src="http://" alt="$1">' : "![$1](http://)", e)
            }
        },
        listUl: {
            title: "Unordered List",
            label: '<i class="fa fa-list-ul"></i>',
            action: function(e) {
                "markdown" == this.getMode() && n("* $1", e)
            }
        },
        listOl: {
            title: "Ordered List",
            label: '<i class="fa fa-list-ol"></i>',
            action: function(e) {
                "markdown" == this.getMode() && n("1. $1", e)
            }
        }
    }, a.defaults = {
        mode: "split",
        height: 500,
        maxsplitsize: 1e3,
        codemirror: {
            mode: "gfm",
            tabMode: "indent",
            tabindex: "2",
            lineWrapping: !0,
            dragDrop: !1,
            autoCloseTags: !0,
            matchTags: !0
        },
        toolbar: ["bold", "italic", "strike", "link", "picture", "blockquote", "listUl", "listOl"],
        lblPreview: "Preview",
        lblCodeview: "Markdown"
    }, a.template = '<div class="uk-markdownarea uk-clearfix" data-mode="split"><div class="uk-markdownarea-navbar"><ul class="uk-markdownarea-navbar-nav uk-markdownarea-toolbar"></ul><div class="uk-markdownarea-navbar-flip"><ul class="uk-markdownarea-navbar-nav"><li class="uk-markdown-button-markdown"><a>{:lblCodeview}</a></li><li class="uk-markdown-button-preview"><a>{:lblPreview}</a></li><li><a data-markdownarea-cmd="fullscreen" data-toggle="tooltip" title="Zen Mode"><i class="fa fa-expand"></i></a></li></ul></div></div><div class="uk-markdownarea-content"><div class="uk-markdownarea-code"></div><div class="uk-markdownarea-preview"><div></div></div></div></div>', a.plugins = {}, a.addPlugin = function(e, t, o) {
        a.plugins[e] = {
            identifier: t,
            cb: o
        }
    }, e.fn.markdownarea = a, e(function() {
        e("textarea[data-uk-markdownarea]").each(function() {
            var t, o = e(this);
            o.data("markdownarea") || (t = new a(o, e.Utils.options(o.attr("data-uk-markdownarea"))))
        })
    }), a
}(jQuery, window, document),
function(e, t, o) {
    e(function() {
        var t = '[data-toggle="navbar-search"]',
            a = '[data-toggle="navbar-search-dismiss"]',
            n = '.navbar-form input[type="text"]',
            r = e("form.navbar-form"),
            i = {
                toggle: function() {
                    r.toggleClass("open");
                    var e = r.hasClass("open");
                    r.find("input")[e ? "focus" : "blur"]()
                },
                dismiss: function() {
                    r.removeClass("open").find('input[type="text"]').blur().val("")
                }
            };
        e(o).on("click", i.dismiss).on("click", t + ", " + n + ", " + a, function(e) {
            e.stopPropagation()
        }).on("click", a, i.dismiss).on("click", t, i.toggle).keyup(function(e) {
            27 == e.keyCode && i.close()
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    function a(t) {
        var o = t.data("message"),
            a = t.data("options");
        o || e.error("Notify: No message specified"), e.notify(o, a || {})
    }
    var n = '[data-toggle="notify"]';
    e(o);
    e(function() {
        e(n).each(function() {
            var t = e(this),
                o = t.data("onload");
            void 0 !== o && setTimeout(function() {
                a(t)
            }, 800), t.on("click", function(e) {
                e.preventDefault(), a(t)
            })
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = {},
        n = {},
        r = function(t) {
            return "string" == e.type(t) && (t = {
                message: t
            }), arguments[1] && (t = e.extend(t, "string" == e.type(arguments[1]) ? {
                status: arguments[1]
            } : arguments[1])), new s(t).show()
        },
        i = function(e, t) {
            if (e)
                for (var o in n) e === n[o].group && n[o].close(t);
            else
                for (var o in n) n[o].close(t)
        },
        s = function(t) {
            this.options = e.extend({}, s.defaults, t), this.uuid = "ID" + (new Date).getTime() + "RAND" + Math.ceil(1e5 * Math.random()), this.element = e(['<div class="tradify-notify-message alert-dismissable">', '<a class="close">&times;</a>', "<div>" + this.options.message + "</div>", "</div>"].join("")).data("notifyMessage", this), this.options.status && (this.element.addClass("alert alert-" + this.options.status), this.currentstatus = this.options.status), this.group = this.options.group, n[this.uuid] = this, a[this.options.pos] || (a[this.options.pos] = e('<div class="tradify-notify tradify-notify-' + this.options.pos + '"></div>').appendTo("body").on("click", ".tradify-notify-message", function() {
                e(this).data("notifyMessage").close()
            }))
        };
    return e.extend(s.prototype, {
        uuid: !1,
        element: !1,
        timout: !1,
        currentstatus: "",
        group: !1,
        show: function() {
            if (!this.element.is(":visible")) {
                var e = this;
                a[this.options.pos].show().prepend(this.element);
                var t = parseInt(this.element.css("margin-bottom"), 10);
                return this.element.css({
                    opacity: 0,
                    "margin-top": -1 * this.element.outerHeight(),
                    "margin-bottom": 0
                }).animate({
                    opacity: 1,
                    "margin-top": 0,
                    "margin-bottom": t
                }, function() {
                    if (e.options.timeout) {
                        var t = function() {
                            e.close()
                        };
                        e.timeout = setTimeout(t, e.options.timeout), e.element.on('mouseover', function() {
                            clearTimeout(e.timeout)
                        }, function() {
                            e.timeout = setTimeout(t, e.options.timeout)
                        })
                    }
                }), this
            }
        },
        close: function(e) {
            var t = this,
                o = function() {
                    t.element.remove(), a[t.options.pos].children().length || a[t.options.pos].hide(), delete n[t.uuid]
                };
            this.timeout && clearTimeout(this.timeout), e ? o() : this.element.animate({
                opacity: 0,
                "margin-top": -1 * this.element.outerHeight(),
                "margin-bottom": 0
            }, function() {
                o()
            })
        },
        content: function(e) {
            var t = this.element.find(">div");
            return e ? (t.html(e), this) : t.html()
        },
        status: function(e) {
            return e ? (this.element.removeClass("alert alert-" + this.currentstatus).addClass("alert alert-" + e), this.currentstatus = e, this) : this.currentstatus
        }
    }), s.defaults = {
        message: "",
        status: "normal",
        timeout: 5e3,
        group: null,
        pos: "top-center"
    }, e.notify = r, e.notify.message = s, e.notify.closeAll = i, r
}(jQuery, window, document),
function(e, t, o) {
    var a = '[data-toggle="offsidebar"]',
        n = ".offsidebar",
        r = "offsidebar-open",
        i = e("body");
    e(function() {
        var t = {
            open: function(e) {
                i.addClass(r)
            },
            close: function() {
                i.removeClass(r)
            },
            toggle: function() {
                i.toggleClass(r)
            }
        };
        e(o).on("click", t.close).on("click", n + "," + a, function(e) {
            e.stopPropagation()
        }).on("click", a, t.toggle)
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = '[data-perform="panel-dismiss"]';
    e(o).on("click", a, function(t) {
        function o() {
            var t = a.parent();
            a.remove(), t.filter(function() {
                var t = e(this);
                return t.is('[class*="col-"]') && 0 === t.children("*").length
            }).remove()
        }
        var a = e(this).closest(".panel");
        e.support.animation ? a.animo({
            animation: "bounceOut"
        }, o) : o()
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = '[data-perform="panel-collapse"]';
    e(a).each(function() {
        var t = e(this),
            o = t.closest(".panel"),
            a = o.find(".panel-wrapper"),
            n = {
                toggle: !1
            };
        a.length || (a = o.children(".panel-heading").nextAll().wrapAll("<div/>").parent().addClass("panel-wrapper"), n = {}), a.collapse(n).on("hide.bs.collapse", function() {
            t.children("em").removeClass("fa-minus").addClass("fa-plus")
        }).on("show.bs.collapse", function() {
            t.children("em").removeClass("fa-plus").addClass("fa-minus")
        })
    }), e(o).on("click", a, function(t) {
        var o = e(this).closest(".panel"),
            a = o.find(".panel-wrapper");
        a.collapse("toggle")
    })
}(jQuery, window, document),
function(e, t, o) {
    function a() {
        this.removeClass(i)
    }
    var n = '[data-perform="panel-refresh"]',
        r = "panel-refresh",
        i = "csspinner",
        s = "standard";
    e(o).on("click", n, function(t) {
        var o = e(this),
            n = o.parents(".panel").eq(0),
            l = o.data("spinner") || s;
        n.addClass(i + " " + l), n.removeSpinner = a, o.trigger(r, [n])
    }), e(".panel.panel-demo").on("panel-refresh", function(e, t) {
        setTimeout(function() {
            t.removeSpinner()
        }, 3e3)
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = '[data-toggle="play-animation"]';
    e(function() {
        var t = e("body, .wrapper");
        e(a).each(function() {
            function o(t) {
                !t.hasClass("anim-running") && e.Utils.isInView(t, {
                    topoffset: n
                }) && (t.addClass("anim-running"), setTimeout(function() {
                    t.addClass("anim-done").animo({
                        animation: i,
                        duration: .7
                    })
                }, r))
            }
            var a = e(this),
                n = a.data("offset"),
                r = a.data("delay") || 100,
                i = a.data("play") || "bounce";
            "undefined" != typeof n && (o(a), t.scroll(function() {
                o(a)
            }))
        }), e(o).on("click", a, function(t) {
            var o = e(this),
                a = o.data("target"),
                n = o.data("play") || "bounce",
                r = e(a);
            r && r && r.animo({
                animation: n
            })
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    if (e.fn.sortable) {
        var a = '[data-toggle="portlet"]';
        e(function() {
            e(a).sortable({
                connectWith: a,
                items: "div.panel",
                handle: ".portlet-handler",
                opacity: .7,
                placeholder: "portlet box-placeholder",
                cancel: ".portlet-cancel",
                forcePlaceholderSize: !0,
                iframeFix: !1,
                tolerance: "pointer",
                helper: "original",
                revert: 200,
                forceHelperSize: !0
            }).disableSelection()
        })
    }
}(jQuery, window, document),
function(e, t, o) {
    var a = '[data-toggle="collapse-next"]',
        n = e(".sidebar .collapse").collapse({
            toggle: !1
        }),
        r = "aside-toggled",
        i = e("body"),
        s = 768;
    e(function() {
        e(o).on("click", a, function(o) {
            if (o.preventDefault(), !(e(t).width() > s && i.hasClass(r))) {
                n.collapse("hide");
                var a = e(this).siblings("ul");
                a.collapse("show")
            }
        }).on("click", ".sidebar > .nav > li", function() {
            i.hasClass(r) && e(t).width() > s && e(".sidebar > .nav > li").not(this).removeClass("open").end().filter(this).toggleClass("open")
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = ".inlinesparkline",
        n = {
            primary: "#5fb5cb",
            success: "#27ae60",
            info: "#22bfe8",
            warning: "#ffc61d",
            danger: "#f6504d"
        };
    e(a).each(function() {
        var t = e(this),
            o = t.data();
        o.barColor && n[o.barColor] && (o.barColor = n[o.barColor]);
        var a = o;
        a.type = o.type || "bar", e(this).sparkline("html", a)
    })
}(jQuery, window, document),
function(e, t, o) {
    var a = "th.check-all";
    e(a).on("change", function() {
        var t = e(this),
            o = t.index() + 1,
            a = t.find('input[type="checkbox"]'),
            n = t.parents("table");
        n.find("tbody > tr > td:nth-child(" + o + ') input[type="checkbox"]').prop("checked", a[0].checked)
    })
}(jQuery, window, document),
function(e, t, o) {
    function a(e) {
        for (var o = e.offsetTop, a = 40; e.offsetParent;) e = e.offsetParent, o += e.offsetTop;
        return o - a - t.pageYOffset
    }

    function n(e) {
        for (var o = e.offsetLeft, a = e.offsetWidth; e.offsetParent;) e = e.offsetParent, o += e.offsetLeft;
        return o - a - t.pageXOffset
    }
    e(function() {
        e('[data-toggle="tooltip"]').tooltip({
            container: "body",
            placement: function(e, t) {
                var o = "top";
                return a(t) < 0 && (o = "bottom"), n(t) < 0 && (o = "right"), o
            }
        })
    })
}(jQuery, window, document),
function(e, t, o) {
    e(function() {
        var t = e("#progressbar"),
            o = t.find(".progress-bar"),
            a = {
                action: "server/upload.php",
                allow: "*.(jpg|jpeg|gif|png)",
                param: "upfile",
                loadstart: function() {
                    o.css("width", "0%").text("0%"), t.removeClass("hidden")
                },
                progress: function(e) {
                    e = Math.ceil(e), o.css("width", e + "%").text(e + "%")
                },
                allcomplete: function(e) {
                    o.css("width", "100%").text("100%"), setTimeout(function() {
                        t.addClass("hidden")
                    }, 250), alert(e)
                }
            };
        new e.upload.select(e("#upload-select"), a), new e.upload.drop(e("#upload-drop"), a)
    })
}(jQuery, window, document),
function(e, t, o) {
    function a(t, o) {
        function r(t, o) {
            var a = new FormData,
                n = new XMLHttpRequest;
            if (o.before(o, t) !== !1) {
                for (var r, i = 0; r = t[i]; i++) a.append(o.param, r);
                for (var s in o.params) a.append(s, o.params[s]);
                n.upload.addEventListener("progress", function(e) {
                    var t = e.loaded / e.total * 100;
                    o.progress(t, e)
                }, !1), n.addEventListener("loadstart", function(e) {
                    o.loadstart(e)
                }, !1), n.addEventListener("load", function(e) {
                    o.load(e)
                }, !1), n.addEventListener("loadend", function(e) {
                    o.loadend(e)
                }, !1), n.addEventListener("error", function(e) {
                    o.error(e)
                }, !1), n.addEventListener("abort", function(e) {
                    o.abort(e)
                }, !1), n.open(o.method, o.action, !0), n.onreadystatechange = function() {
                    if (o.readystatechange(n), 4 == n.readyState) {
                        var t = n.responseText;
                        if ("json" == o.type) try {
                            t = e.parseJSON(t)
                        } catch (a) {
                            t = !1
                        }
                        o.complete(t, n)
                    }
                }, n.send(a)
            }
        }
        if (!e.support.ajaxupload) return this;
        if (o = e.extend({}, a.defaults, o), t.length) {
            if ("*.*" !== o.allow)
                for (var i, s = 0; i = t[s]; s++)
                    if (!n(o.allow, i.name)) return void("string" == typeof o.notallowed ? alert(o.notallowed) : o.notallowed(i, o));
            var l = o.complete;
            if (o.single) {
                var d = t.length,
                    c = 0;
                o.complete = function(e, a) {
                    c += 1, l(e, a), d > c ? r([t[c]], o) : o.allcomplete(e, a)
                }, r([t[0]], o)
            } else o.complete = function(e, t) {
                l(e, t), o.allcomplete(e, t)
            }, r(t, o)
        }
    }

    function n(e, t) {
        var o = "^" + e.replace(/\//g, "\\/").replace(/\*\*/g, "(\\/[^\\/]+)*").replace(/\*/g, "[^\\/]+").replace(/((?!\\))\?/g, "$1.") + "$";
        return o = "^" + o + "$", null !== t.match(new RegExp(o))
    }
    var r = function(t, o) {
        var n = this,
            i = e(t),
            o = e.extend({}, a.defaults, r.defaults, o);
        i.data("uploadSelect") || (this.element = i.on("change", function() {
            a(n.element[0].files, o)
        }), i.data("uploadSelect", this))
    };
    r.defaults = {};
    var i = function(t, o) {
        var n = e(t),
            o = e.extend({}, a.defaults, i.defaults, o),
            r = !1;
        n.data("uploadDrop") || (n.on("drop", function(e) {
            e.dataTransfer && e.dataTransfer.files && (e.stopPropagation(), e.preventDefault(), n.removeClass(o.dragoverClass), a(e.dataTransfer.files, o))
        }).on("dragenter", function(e) {
            e.stopPropagation(), e.preventDefault()
        }).on("dragover", function(e) {
            e.stopPropagation(), e.preventDefault(), r || (n.addClass(o.dragoverClass), r = !0)
        }).on("dragleave", function(e) {
            e.stopPropagation(), e.preventDefault(), n.removeClass(o.dragoverClass), r = !1
        }), n.data("uploadDrop", this))
    };
    return i.defaults = {
        dragoverClass: "dragover"
    }, e.upload = {
        select: r,
        drop: i
    }, e.support.ajaxupload = function() {
        function e() {
            var e = o.createElement("INPUT");
            return e.type = "file", "files" in e
        }

        function a() {
            var e = new XMLHttpRequest;
            return !!(e && "upload" in e && "onprogress" in e.upload)
        }

        function n() {
            return !!t.FormData
        }
        return e() && a() && n()
    }(), e.support.ajaxupload && e.event.props.push("dataTransfer"), a.defaults = {
        action: "",
        single: !0,
        method: "POST",
        param: "files[]",
        params: {},
        allow: "*.*",
        type: "text",
        before: function(e) {},
        loadstart: function() {},
        load: function() {},
        loadend: function() {},
        error: function() {},
        abort: function() {},
        progress: function() {},
        complete: function() {},
        allcomplete: function() {},
        readystatechange: function() {},
        notallowed: function(e, t) {
            alert("Only the following file types are allowed: " + t.allow)
        }
    }, e.xhrupload = a, a
}(jQuery, window, document),
function(e, t, o) {
    var a = ".user-block-status";
    e(o).on("click", a, function(t) {
        t.stopPropagation();
        var o = e(this),
            a = o.find(".dropdown-menu > li > a").filter(t.target).html(),
            n = o.find(".btn");
        n.html(a), e(".user-block .user-block-picture .user-block-status").html(a), o.hasClass("open") && n.dropdown("toggle")
    })
}(jQuery, window, document),
function(e, t, o) {
    "use strict";
    var a = e("html"),
        n = e(t);
    e.support.transition = function() {
        var e = function() {
            var e, t = o.body || o.documentElement,
                a = {
                    WebkitTransition: "webkitTransitionEnd",
                    MozTransition: "transitionend",
                    OTransition: "oTransitionEnd otransitionend",
                    transition: "transitionend"
                };
            for (e in a)
                if (void 0 !== t.style[e]) return a[e]
        }();
        return e && {
            end: e
        }
    }(), e.support.animation = function() {
        var e = function() {
            var e, t = o.body || o.documentElement,
                a = {
                    WebkitAnimation: "webkitAnimationEnd",
                    MozAnimation: "animationend",
                    OAnimation: "oAnimationEnd oanimationend",
                    animation: "animationend"
                };
            for (e in a)
                if (void 0 !== t.style[e]) return a[e]
        }();
        return e && {
            end: e
        }
    }(), e.support.requestAnimationFrame = t.requestAnimationFrame || t.webkitRequestAnimationFrame || t.mozRequestAnimationFrame || t.msRequestAnimationFrame || t.oRequestAnimationFrame || function(e) {
        t.setTimeout(e, 1e3 / 60)
    }, e.support.touch = "ontouchstart" in t && navigator.userAgent.toLowerCase().match(/mobile|tablet/) || t.DocumentTouch && document instanceof t.DocumentTouch || t.navigator.msPointerEnabled && t.navigator.msMaxTouchPoints > 0 || t.navigator.pointerEnabled && t.navigator.maxTouchPoints > 0 || !1, e.support.mutationobserver = t.MutationObserver || t.WebKitMutationObserver || t.MozMutationObserver || null, e.Utils = {}, e.Utils.debounce = function(e, t, o) {
        var a;
        return function() {
            var n = this,
                r = arguments,
                i = function() {
                    a = null, o || e.apply(n, r)
                },
                s = o && !a;
            clearTimeout(a), a = setTimeout(i, t), s && e.apply(n, r)
        }
    }, e.Utils.removeCssRules = function(e) {
        var t, o, a, n, r, i, s, l, d, c;
        e && setTimeout(function() {
            try {
                for (c = document.styleSheets, n = 0, s = c.length; s > n; n++) {
                    for (a = c[n], o = [], a.cssRules = a.cssRules, t = r = 0, l = a.cssRules.length; l > r; t = ++r) a.cssRules[t].type === CSSRule.STYLE_RULE && e.test(a.cssRules[t].selectorText) && o.unshift(t);
                    for (i = 0, d = o.length; d > i; i++) a.deleteRule(o[i])
                }
            } catch (u) {}
        }, 0)
    }, e.Utils.isInView = function(t, o) {
        var a = e(t);
        if (!a.is(":visible")) return !1;
        var r = n.scrollLeft(),
            i = n.scrollTop(),
            s = a.offset(),
            l = s.left,
            d = s.top;
        return o = e.extend({
            topoffset: 0,
            leftoffset: 0
        }, o), d + a.height() >= i && d - o.topoffset <= i + n.height() && l + a.width() >= r && l - o.leftoffset <= r + n.width() ? !0 : !1
    }, e.Utils.options = function(t) {
        if (e.isPlainObject(t)) return t;
        var o = t ? t.indexOf("{") : -1,
            a = {};
        if (-1 != o) try {
            a = new Function("", "var json = " + t.substr(o) + "; return JSON.parse(JSON.stringify(json));")()
        } catch (n) {}
        return a
    }, e.Utils.events = {}, e.Utils.events.click = e.support.touch ? "tap" : "click", e.langdirection = "rtl" == a.attr("dir") ? "right" : "left", e(function() {
        if (e.support.mutationobserver) {
            var t = new e.support.mutationobserver(e.Utils.debounce(function(t) {
                e(o).trigger("domready")
            }, 300));
            t.observe(document.body, {
                childList: !0,
                subtree: !0
            })
        }
    }), a.addClass(e.support.touch ? "touch" : "no-touch")
}(jQuery, window, document),
function(e, t, o) {
    if ("undefined" == typeof e) throw new Error("This application's JavaScript requires jQuery");
    e(t).load(function() {
        e(".scroll-content").slimScroll({
            height: "250px"
        })
    }), e(function() {
        FastClick.attach(o.body), e('a[href="#"]').each(function() {
            this.href = "javascript:void(0);"
        }), e("[data-toggle=popover]").popover(), e(".slider").slider(), e(".chosen-select").chosen(), e(".filestyle").filestyle()
    })
}(jQuery, window, document);

// preloader
$(window).load(function(){
            setTimeout(function(){
                $('#preloader').velocity({
                    opacity : 0.1,
                    translateY: "-80px"
                }, {
                    duration: 400,
                    complete: function(){
                    $('#overlayLoader').velocity({
                    translateY : "-100%"
                }, {
                    duration: 1000,
                    easing: [0.7,0,0.3,1],
                    complete: function(){
                        $('body').addClass('animate-border divide');
                    }
                })  
                    }
                })
            },1000)
        })




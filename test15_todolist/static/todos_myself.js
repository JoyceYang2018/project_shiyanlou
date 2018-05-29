$(function () {

//    创建todo项的模型
//    todo项模型有title内容，order排序号与done完成与否的属性
    var Todo = Backbone.Model.extend({

    //    todo项的默认值
        defaults: function () {
            return{
                title:"empty todo...",
                order:Todo.nextOrder(),
                done:0
            };
        },

    //    保证每个TODO都有title
        initialize:function () {
            if (!this.get("title")){
                this.set({"title":this.defaults().title});
            }
        },

    //    toggle函数改变done的状态
        toggle: function () {
            this.save({done: 1-this.get("done")});
        }
    });





//创建todo项的集合
    var TodoList = Backbone.Collection.extend({
        model:Todo,
    //    mysql server
        url:'/todos',

    //    过滤出所有已完成的todo
        done:function () {
            return this.filter(function (todo) {
                if (todo.get('done')==1) {
                    return True;
                }
            });
        }

    //    过滤出所有未完成的todo
        remaining:function () {
            return this.without.apply(this,this.done());
        },

    //    因为在数据库中todo项是按无序的GUID排放的，所以需要order属性，生成order序列号
        nextOrder:function () {
            if(!this.length) return 1;
            return this.last().get('order')+1;
        }

    //    todo项按照插入顺序排序
        comparator:function (todo) {
            return todo.get('order');
        }


    });


//    创建集合的全局变量
    var Todos = new TodoList;


    var TodoView = Backbone.View.extent({

    //    表示todo项的DOM元素是li
        tagName:"li",

    //    缓存单个todo项的模板函数
        template: _.template($('#item-template').html()),

    //    todo项的DOm事件
        events:{
            "click .toggle":"toggleDone",
            "dblclick .view":"edit",
            "click a.destroy":"clear",
            "keypress .edit":"updateOnEnter",
            "blur .edit":"close"
        },

    //    TodoView监听它所对应的模型，在模型发生变化市重新渲染。

        initialize:function () {
            this.listenTo(this.model,'change',this.render);
            this.listenTo(this.model,'destroy',this.remove);
        },

    //    重新渲染todo项的内容
        render:function () {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.toggleClass('done',this.model.get('done'));
            this.input = this.$('.edit');
            return this
        },


    //    切换该模型的完成状态
        toggleDone:function () {
            this.model.toggle();
        },


    //    切换该视图到编辑模式，显示输入域
        edit:function () {
            this.$el.addClass("editing");
            this.input.focus();
        },



    //    关闭编辑模式并保存变化
        close:function () {
            var value=this.input.val();
            if (!value){
                this.clear();
            }else {
                this.model.save({title:value});
                this.$el.removeClass("editing");
            }
        },


    //    当你单击回车，关闭编辑模式
        updateOnEnter:function () {
            if(e.keyCode==13) this.close();
        },


    //    移除某一项，销毁它的模型
        clear:function () {
            this.model.destroy();
        }
    });







    var AppView = Backbone.View.extend({

    // 该视图引用 #todoapp 元素
    el: $("#todoapp"),

    // 缓存 #stats-template 部分的模版函数
    statsTemplate: _.template($('#stats-template').html()),

    // 委托事件，包括创建新todo，清理所有的已完成项 和 标记全部 todo 为已完成。
    events: {
      "keypress #new-todo":  "createOnEnter",
      "click #clear-completed": "clearCompleted",
      "click #toggle-all": "toggleAllComplete"
    },

    // 初始化，做一些元素绑定和事件监听。

    initialize: function() {

      //获取主输入域
      this.input = this.$("#new-todo");
      //获取 'Mark all as complete' 左边的那个 checkbox
      this.allCheckbox = this.$("#toggle-all")[0];

      this.listenTo(Todos, 'add', this.addOne);
      this.listenTo(Todos, 'reset', this.addAll);
      this.listenTo(Todos, 'all', this.render);

      this.footer = this.$('footer');
      this.main = $('#main');

      Todos.fetch();
    },

    // 渲染改变的部分
    render: function() {
      var done = Todos.done().length;
      var remaining = Todos.remaining().length;

      if (Todos.length) {
        this.main.show();
        this.footer.show();
        this.footer.html(this.statsTemplate({done: done, remaining: remaining}));
      } else {
        this.main.hide();
        this.footer.hide();
      }

      this.allCheckbox.checked = !remaining;
    },

    // 新加一个 todo 项视图到`<ul>`元素中
    addOne: function(todo) {
      var view = new TodoView({model: todo});
      this.$("#todo-list").append(view.render().el);
    },

    // 一次性加入所有的 todo 项视图
    addAll: function() {
      Todos.each(this.addOne);
    },

    // 当你在主输入域敲击回车时会创建一个新 todo 模型并清空主输入域
    createOnEnter: function(e) {
      if (e.keyCode != 13) return;
      if (!this.input.val()) return;

      Todos.create({title: this.input.val()});
      this.input.val('');
    },

    // 清除所有的 todo 项并销毁它们的模型
    clearCompleted: function() {
      _.invoke(Todos.done(), 'destroy');
      return false;
    },

    toggleAllComplete: function () {
      var done = this.allCheckbox.checked;
      Todos.each(function (todo) { todo.save({'done': done}); });
    }

    });

  // 最后，创建 **AppView** 的实例，大功告成
var App = new AppView;





})
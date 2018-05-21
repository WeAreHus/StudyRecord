$(function(){

   //$('#box').dialog();
   $.parser.parse('#box');
});

$.parser.auto = false;
$.parser.onComplete = function (){
    alert('UI解析完毕！');
};


// //parser属性值默认为true  (定义是否自动解析EasyUI组件)
// //关闭自动解析功能，放在$(function() {})外
// $parser.auto.auto = false;


// //解析所有UI
// $parser.parse();
// //解析指定UI
// $parser.parse('#box');
// //使用指定UI解析，必须要设置父类容器才可以解析到。
// <div class="...">
//     <div........>
//     </div>
// </div>
//
// //UI组件解析完毕后执行，放在$(function () {})外
// $parser.onComplete = function() {
//     alert('UI组件解析完毕！');
// };


    

$.ajax({
    type: "post",
     url:'test.json',
    cache: false,
    dataType : "json",
    success: function(data){

        a = data[0].url_01;
        b = data[1].url_02;
        c = data[2].url_03;
        d = data[3].url_04;
        e = data[4].url_05;





var setting = {
			data: {
				simpleData: {
					enable: true
				}
			}
		};




		var zNodes =[
			{ id:1, pId:0, name:"第一级URL", open:true},
			{ id:2,pId:1, name:a},
			{ id:11, pId:1, name:"第二级URL", open:true},
			{ id:12,pId:11,name:b},
			{ id:111, pId:11, name:"第三级URL",open:true},
			{ id:113,pId:111,name:c},
			{ id:1111,pId:111, name:"第四级URL", open:true},
			{ id:1112,pId:1111, name:d},
			{ id:11111,pId:1111,name:"第五级URL", open:true},
			{ id:11112,pId:11111,name:e}
		];
		
		
		$(document).ready(function(){
			$.fn.zTree.init($("#treeDemo"), setting, zNodes);
			setCheck();
		
		});
    }
                             });

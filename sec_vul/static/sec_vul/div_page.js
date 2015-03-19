
 var pageSize = 10;//每页显示的记录条数
 var curPage=0;
 var lastPage;
 var direct=0;
 var len;
 var page;
 $(document).ready(function(){    
     len =$("#table tr").length;
        page=len % pageSize==0 ? len/pageSize : Math.floor(len/pageSize)+1;//根据记录条数，计算页数
      //  alert("page==="+page);
        curPage=1;
        displayPage(1);//显示第一页
        $("#btn1").click(function(){
         curPage=1;
         document.write("The 1 page");
         displayPage();
     });
        $("#btn2").click(function(){
         direct=-1;
         displayPage();
     });
        $("#btn3").click(function(){
         direct=1;
         displayPage();
     });
        $("#btn4").click(function(){
         curPage=page;
         displayPage();
     });
 });
 
 function displayPage(){
  if((curPage <=1 && direct==-1) || (curPage >= page && direct==1)){
   direct=0;
   alert("已经是第一页或者最后一页了");
   return;
  }
  lastPage = curPage;
  curPage = (curPage + direct + len) % len;
     var begin=(curPage-1)*pageSize;//起始记录号
     var end = begin + pageSize;
  if(end > len ) end=len;
     $("#table tr").hide();
     $("#table tr").each(function(i){
         if(i>=begin && i<end)//显示第page页的记录
             $(this).show();
     });

 }

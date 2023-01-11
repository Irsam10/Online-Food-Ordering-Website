
// $("#car-btn").on("click",function(event){
//     const parent = $(this).parents('.card');
//     const title= $('.card-title',parent).text();
//     console.log(parent)
//     //console.log(title+"hello");
//     $.ajax({
//         url: '/addtocart',
//         type: 'POST',
//         data:{
//             javascript_data: title
//             //urlLink:
//         },
//         success: function (response){
//             alert("Added To cart")
//         },
//         error: function (response){
//         }
//     });
// })
$(document).on("click",'#car-btn',function(event){
    const parent = $(this).parents('.card');
    const title= $('.card-title',parent).text()
    $.ajax({
        url: '/addtocart',
        type: 'POST',
        data:{
            javascript_data: title
            //urlLink:
        },
        success: function (response){
            alert("Added To cart")
        },
        error: function (response){
        }
    });

})
$(document).on("click",'#add-btn',function(event){
    const parent = $(this).parents('.card');
    const title= $('.card-title',parent).text()
    $.ajax({
        url: '/addtocart',
        type: 'POST',
        data:{
            javascript_data: title
            //urlLink:
        },
        success: function (response){
            alert("Added To cart")
        },
        error: function (response){
        }
    });

})


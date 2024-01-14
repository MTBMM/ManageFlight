function pay(){
        console.log("aaaaaa")
        fetch("/api/pay", {
                method: "post"

        }).then( res => res.json() ).then( data => {
                if ( data.code == 200 ){
                     var s = document.getElementById("success")
                       s.innerText = "Thành công"
                }
        })
}
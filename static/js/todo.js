$(document).ready(function(){
    $("#comp").on("click", function() {
        $.get(
            "/comp/",
            function(resText, statusText, xhr) {
                if (statusText == "success") {
                    updatePage(resText); 
                }
                if (statusText == "error") {
                    alert("An unexpected error occured");
                }
        });
    });    
});

function updatePage(response) {
    document.getElementById("ijob").style.display = "hidden";
    document.getElementById("cjob").style.display = "block";
    document.getElementById("demo").innerHTML = response[0]["title"];
}

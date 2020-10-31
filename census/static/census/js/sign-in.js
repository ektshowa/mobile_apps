$(document).ready(function() {
    /*$.ajax(
        {type:"post",
         url: "http://127.0.0.1:9090/api/sign_in/",
        headers: {'Authorization': 'Token 73f6527b44a215c593d10d1fdf887541a8db3fad'}, 
        username: 'pre_agent_four_nom_agent_four',
        password: 'pre_agent_four_123',
        success: function(data){
            console.log(data);
        }
    });*/

    if (localStorage) {
        var user_token = localStorage.getItem("user_token");
        var auth_token = localStorage.getItem("auth_token");
        var token = JSON.parse(auth_token);

        try {
            var auth_token = "Token " + token.auth_token.auth_token;
        }
        catch(err) {
            console.log(err.message);
            var auth_token = "Token ";
        }
        if (!token.auth_token.auth_token) {
            var username = $("#username").val();
            var password = $("#password").val();
            $.ajax({
                type: "post",
                url: "http://127.0.0.1:9090/api/api_token_auth/",
                data: {username: username,
                        password: password},
                success: function(resp) {
                    console.log(resp);
                    console.log("token " + resp["token"]);
                    const token = { token: resp["token"] };
                    const json = JSON.stringify(token);
                    console.log(json);
                    localStorage.setItem("user_token", json);
                }
            });
        }
        
    }

    $("#btn-submit").click(function(e) {
        e.preventDefault();
        var auth_token = localStorage.getItem("auth_token");
        var token = JSON.parse(auth_token);

        try {
            var auth_token = "Token " + token.auth_token.auth_token;
        }
        catch(err) {
            console.log(err.message);
            var auth_token = "Token ";
        }
        var form_data = $("form").serializeArray().reduce(
            function(obj, item) {
                obj[item.name] = item.value;
                return obj;
            }, {});
        console.log(form_data);
        $.ajax({
            url: Census.Settings.signInUrl,
            type: "post",
            headers: { 'Authorization': auth_token },
            data: form_data,
            dataType: "json",
            success: function(resp) {
                console.log("CHANGE PAGE ONE");
                console.log(resp);
                $.mobile.navigate("#census_agent_page");
                console.log("CHANGE PAGE");
                //$.mobile.changePage("census-agent-page.html");
                
                return;
            }
        });
    });

    $("#btn_logout").click(function(e) {
        e.preventDefault();
        $.ajax({
            url: Census.Settings.signOutUrl,
            type: "get",
            success: function(resp) {
                console.log("LOGGED OUT");
                console.log(resp);
                $.mobile.navigate("#login_page");
                return;
            }
        });
    });
});
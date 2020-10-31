var get_provinces_choices = function(select_id) {
    let send_request = false;
    var local_province = localStorage.getItem("local_province");
    if (local_province === null) {
        send_request = true;
    }
    let province = "";
    var el_selector = "#" + select_id;
    
    try {
        if (!send_request) {
            province = JSON.parse(local_province);
            console.log(province);
            if (province.local_province === undefined ||
                        province["local_province"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var province_arr = [];
            $.get(Census.Settings.provincesUrl,
                function(data) {
                    if (data) {
                        console.log("PROVINCE SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var province_obj = {option_name: option_name,
                                                option_value: option_value};
                            province_arr[i] = province_obj;
                            //console.log("VALUES " + option_value + " " + option_name);
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);
                        }
                        $(el_selector).selectmenu();
                        $(el_selector).selectmenu("refresh", true);
                        const province_storage = {
                            local_province: province_arr
                        };
                        const province_json = JSON.stringify(province_storage);
                        localStorage.setItem("local_province", province_json);
                    }
                });
        }
        else {
            province = province["local_province"];
            for (var i=0; i<province.length; i++) {
                console.log("PROVINCE EXISTS HERE");
                var option_name = province[i].option_name;
                var option_value = province[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        marrital_status = "";
    }
};

$(document).ready(function() {
    if (localStorage) {
        get_provinces_choices("select_province");
        get_provinces_choices("team_province");
        
        $("#select_province").change(function(e) {
            e.preventDefault();
            var el_select = "#select_city";
            $("option", el_select).not(':eq(0)').remove();
            var province_id = $(this).find(":selected").val();
            $.get(Census.Settings.citiesUrl,
                { province_id: province_id },
                function(data) {
                    //console.log("CITIES SUCCESS");
                    //console.log(data);
                    for (var i=0; i<data.length; i++) {
                        option_name = data[i].name;
                        option_value = data[i].pk.toString();
                        //var city_obj = {option_name: option_name,
                        //                option_value: option_value};
                        //citiesArr[i] = city_obj;
                        //console.log("option_name="+option_name+" option_value="+option_value);
                        $("<option/>").attr("value", option_value).text(option_name).appendTo("#select_city");
                    }
                    $('#select_city').selectmenu();
                    $('#select_city').selectmenu('refresh', true);
                }

            );
        });
        $("#select_city").change(function(e) {
            e.preventDefault();
            var el_select = "#select_commune";
            $("option", el_select).not(':eq(0)').remove();
            var city_id = $(this).find(":selected").val();
            $.get(Census.Settings.communesUrl,
                { city_id: city_id },
                function(data) {
                    console.log("COMMUNES SUCCESS");
                    console.log(data);
                    for (var i=0; i<data.length; i++) {
                        option_name = data[i].name;
                        option_value = data[i].pk.toString();
                        console.log("option_name="+option_name+" option_value="+option_value);
                        $("<option/>").attr("value", option_value).text(option_name).appendTo("#select_commune");
                    }
                    $('#select_commune').selectmenu();
                    $('#select_commune').selectmenu('refresh', true);
                }
            );
        });
    }
    var emailAddressIsValid = function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    };
    var passwordsMatch = function(password, passwordConfirm) {
        return password === passwordConfirm;
    };
    $(document).delegate("#agent_address", "pagebeforecreate", function () {

        var $agentSignUpPage = $("#agent_address"),
            $btnSubmit = $("#agent_sign_submit", $agentSignUpPage);

        $btnSubmit.off("tap").on("tap", function () {
           var $ctnErr = $("#ctn_err"),
               $censusTeam = $("#census_team"),
               $firstName = $("#first_name"),
               $lastName = $("#last_name"),
               $email = $("#email"),
               $phoneNumber1 = $("#phone_number_1"),
               $phoneNumber2 = $("#phone_number_2"),
               $password = $("#password"),
               $passwordConfirm = $("#password_confirm"),
               $selectProvince = $("#select_province"),
               $selectCity = $("#select_city"),
               $selectCommune = $("#select_commune"),
               $neighborhood = $("#neighborhood"),
               $houseNum = $("#house_num");

           var censusTeam = $censusTeam.val().trim(),
               firstName = $firstName.val().trim(),
               lastName = $lastName.val().trim(),
               email = $email.val().trim(),
               phoneNumber1 = $phoneNumber1.val().trim(),
               phoneNumber2 = $phoneNumber2.val().trim(),
               password = $password.val().trim(),
               passwordConfirm = $passwordConfirm.val().trim(),
               selectProvince = $selectProvince.val().trim(),
               selectCity = $selectCity.val().trim(),
               selectCommune = $selectCommune.val().trim(),
               neighborhood = $neighborhood.val().trim(),
               houseNum = $houseNum.val().trim(),
               invalidInput = false,
               invisibleStyle = "bi-invisible",
               invalidInputStyle = "bi-invisible-input";

            $ctnErr.removeClass().addClass(invisibleStyle);
            $censusTeam.removeClass(invalidInputStyle);
            $firstName.removeClass(invalidInputStyle);
            $lastName.removeClass(invalidInputStyle);
            $email.removeClass(invalidInputStyle);
            $phoneNumber1.removeClass(invalidInputStyle);
            $phoneNumber2.removeClass(invalidInputStyle);
            $password.removeClass(invalidInputStyle);
            $passwordConfirm.removeClass(invalidInputStyle);
            $selectProvince.removeClass(invalidInputStyle);
            $selectCity.removeClass(invalidInputStyle);
            $selectCommune.removeClass(invalidInputStyle);
            $neighborhood.removeClass(invalidInputStyle);
            $houseNum.removeClass(invalidInputStyle);

            if (censusTeam.length === 0) {
                $firstName.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (firstName.length === 0) {
                $firstName.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (lastName.length === 0) {
                $lastName.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (email.length === 0) {
                $email.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (phoneNumber1.length === 0) {
                $phoneNumber1.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (phoneNumber2.length === 0) {
                $phoneNumber2.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (password.length === 0) {
                $password.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (passwordConfirm.length === 0) {
                $passwordConfirm.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (selectProvince.length === 0) {
                $selectProvince.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (selectCity.length === 0) {
                $selectCity.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (selectCommune.length === 0) {
                $selectCommune.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (neighborhood.length === 0) {
                $neighborhood.addClass(invalidInputStyle);
                invalidInput = true;
            }
            if (houseNum.length === 0) {
                $houseNum.addClass(invalidInputStyle);
                invalidInput = true;
            }
            // Make sure that all the required fields have values.
            if (invalidInput) {
                $ctnErr.html("<p>S'il vous pla&icirc;t remplissez les donn&eacute;es requise.</p>");
                $ctnErr.addClass("bi-ctn-err").slideDown();
                return;
            }
            if (!emailAddressIsValid(email)) {
                $ctnErr.html("<p>S'il vous pla&icirc;t entrez une valid adresse courriel</p>");
                $ctnErr.addClass("bi-ctn-err").slideDown();
                $email.addClass(invalidInputStyle);
                return;
            }
            if (!passwordsMatch(password, passwordConfirm)) {
                $ctnErr.html("<p>Les mots de passe sont diff&eacute;rents.</p>");
                $ctnErr.addClass("bi-ctn-err").slideDown();
                $password.addClass(invalidInputStyle);
                $passwordConfirm.addClass(invalidInputStyle);
                return;
            }
        });
    });
    $("input[name=zone_type]").click(function(e) {
        var value = $("input[name=zone_type]:checked").val();
        
        if (value == "zone_type_rural") {
            console.log("CLICKED " + value);
            $("#div_team_city").addClass("bi-invisible");
            $("#div_team_commune").addClass("bi-invisible");
            $("#div_team_territory").removeClass("bi-invisible");
        }
        else if (value == "zone_type_urban") {
            console.log("CLICKED " + value);
            $("#div_team_territory").addClass("bi-invisible");
            $("#div_team_city").removeClass("bi-invisible");
            $("#div_team_commune").removeClass("bi-invisible");
        }
    });
    $("#team_province").change(function(e) {
        e.preventDefault();
        var selected_zone_type = $("input[name=zone_type]:checked").val();
        if (selected_zone_type == "zone_type_rural") {
            var el_select = "#team_territory";
        }
        else if (selected_zone_type == "zone_type_urban") {
            var el_select = "#team_city";
        }
        
        $("option", el_select).not(':eq(0)').remove();
        var province_id = $(this).find(":selected").val();
        $.get(Census.Settings.citiesUrl,
            { province_id: province_id },
            function(data) {
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    $("<option/>").attr("value", option_value).text(option_name).appendTo(el_select);
                }
                $(el_select).selectmenu();
                $(el_select).selectmenu('refresh', true);
            }

        );
    });
    $("#team_city").change(function(e) {
        e.preventDefault();
        var el_select = "#team_commune";
        $("option", el_select).not(':eq(0)').remove();
        var city_id = $(this).find(":selected").val();
        $.get(Census.Settings.communesUrl,
            { city_id: city_id },
            function(data) {
                console.log("COMMUNES SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    console.log("option_name="+option_name+" option_value="+option_value);
                    $("<option/>").attr("value", option_value).text(option_name).appendTo(el_select);
                }
                $(el_select).selectmenu();
                $(el_select).selectmenu('refresh', true);
            }
        );
    });
    $(".smallest_unit").change(function(e) {
        e.preventDefault();
        var el_clicked_id = $(this).attr("id");
        el_clicked_id = "#" + el_clicked_id;
        if (el_clicked_id == "#team_commune") {
            var request_data = {
                province_id: $("#team_province").find(":selected").val(),
                city_id: $("#team_city").find(":selected").val(),
                commune_id: $(this).find(":selected").val()
            };
        }
        else if (el_clicked_id == "#team_territory"){
            var request_data = {
                province_id: $("#team_province").find(":selected").val(),
                territory_id: $(this).find(":selected").val() 
            };
        }
        //var smallest_unit_id = $(el_clicked_id + ":selected").val();
        var el_select = "#census_team";
        $("option", el_select).not(':eq(0)').remove();
        $.get(Census.Settings.censusTeamsUrl,
            request_data,
            function(data) {
                console.log("CENSUS TEAMS SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].code + "--" + data[i].name;
                    option_value = data[i].pk.toString();
                    $("<option/>").attr("value", option_value).text(option_name).appendTo(el_select);
                }
                $(el_select).selectmenu();
                $(el_select).selectmenu('refresh', true);
            }
        );

    });
    $("#agent_sign_submit").click(function(e) {
        e.preventDefault();
        $.each($("#agent_info").find("input"), function() {
            $("#census_agent").append($(this).clone()).hide();
        });
        var team_html = '<input type="hidden" id="hidden_team" name="hidden_team" value="">';
        $("#census_agent").append(team_html);
        var team_val = $("#census_team").val();
        $("#hidden_team").val(team_val);
        //$("#census_agent").append($("#census_team").clone());
        var form_data = $("form#census_agent").serializeArray().reduce(
            function(obj, item) {
                obj[item.name] = item.value;
                return obj;
            }, {});
        console.log(form_data);
        $.ajax({
            url: Census.Settings.agentSignUpUrl,
            type: "post",
            data: form_data,
            dataType: "json",
            success: function(resp) {
                console.log(resp);
                if (resp.success == true) {
                    if (localStorage) {
                        var username = resp.data["username"];
                        var auth_token = {"auth_token": resp.data["auth_token"]};
                        token = {"username": username, "auth_token": auth_token};
                        auth_token = JSON.stringify(token);
                        console.log("USER TOKEN: " + auth_token);
                        localStorage.setItem("auth_token", auth_token);
                    }
                    $.mobile.navigate("#login_page");
                    return;
                }
                else {/*
                    if (resp.extra.msg) {
                        switch (resp.extra.msg) {
                            case Census.ApiMessages.DB_ERROR:
                            case Census.ApiMessages.COULD_NOT_CREATE_USER:
                                err_mess = "Une erreur s'est produite. S'il vous plaît reessayez ";
                                err_mess =+ "Contactez votre superviseur si l'erreur se reproduit";
                                $("#ctn_err").html(err_mess);
                                $("#ctn_err").addClass("bi-ctn-err").slideDown();
                                break;
                            case Census.ApiMessages.EMAIL_ALREADY_EXISTS:
                                err_mess = "L'adresse courriel utilis&eacute;e existe d&eacute;j&agrave;";
                                $("#ctn_err").html(err_mess);
                                $("#email").addClass(invalidInputStyle);
                            case Census.ApiMessages.PHONE_1_ALREADY_EXISTS: 
                                err_mess = "Le num&eacute;ro de t&eacute;l&eacute;phone principal utilis&eacute; existe d&eacute;j&agrave;";
                                $("#ctn_err").html(err_mess);
                                $("#phone_number_1").addClass(invalidInputStyle);
                            case Census.ApiMessages.PHONE_2_ALREADY_EXISTS: 
                                err_mess = "Le num&eacute;ro de t&eacute;l&eacute;phone secondaire utilis&eacute; existe d&eacute;j&agrave;";
                                $("#ctn_err").html(err_mess);
                                $("#phone_number_2").addClass(invalidInputStyle);
                        }
                    }*/
                }

            },
            error: function(err) {
                console.log(e.message);
                err_mess = "Erreur, il y a eu un probl&egrave;me. Vous n'avez pas &eacute;t&eacute; enregistr&eacute;";
                err_mess =+ "S'il vous plaît reessayez";
                $("#ctn_err").html(err_mess);
                $("#ctn_err").addClass("bi-ctn-err").slideDown();
            }
        });
    });
    var get_auth_token = function() {
        var auth_token = localStorage.getItem("auth_token");
        var token = JSON.parse(auth_token);
    
        try {
            var auth_token = "Token " + token.auth_token.auth_token;
        }
        catch(err) {
            console.log(err.message);
            var auth_token = "Token ";
        }
        return auth_token;
    };
    $("#btn-submit-login").click(function(e) {
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
        var form_data = $("form#login_form").serializeArray().reduce(
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
            },
            error: function(xhr, textStatus) {
               if (xhr.status == 401) {
                   console.log(xhr.status);
                   console.log(textStatus);
                   console.log(auth_token);
                   old_token = token.substring(6, token.length);
                   if (old_token.length > 3) {
                       var is_valid_token = false;
                   }
               } 
            }
        });
        /*
        var get_new_auth_token = function(is_valid_token) {
            if (!is_valid_token) {
                $.ajax({
                    url: Census.Settings.requestAuthToken,
                    type: "get",

                })
            }
        };*/
    });
    $("#btn_logout").click(function(e) {
        e.preventDefault();
        var auth_token = get_auth_token();
        $.ajax({
            url: Census.Settings.signOutUrl,
            type: "get",
            headers: { 'Authorization': auth_token },
            success: function(resp) {
                console.log("LOGGED OUT");
                console.log(resp);
                $.mobile.navigate("#login_page");
                return;
            }
        });
    });
    
});
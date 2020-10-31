var CensusHouseholdRecord = CensusHouseholdRecord || {};

CensusHouseholdRecord.get_provinces_choices = function(select_id) {
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

$(document).ready(function () {
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

    $("input[name=filled_by]").click(function() {
        var filled_by = $("input[name=filled_by]:checked").val();
        if (filled_by == "househead") {
            var agent_id = $("#census_agent_id").val();
            if (!agent_id) {
                alert("Remplissez le numero de l'agent avant de continuer");
                $(this).prop('checked', false);
            }
            else {
                var token = get_auth_token();
                $.ajax({
                    url: Census.Settings.householdRecordsUrl,
                    type: "get",
                    headers: { 'Authorization': token},
                    data: { agent_id: agent_id },
                    dataType: "json",
                    success: function(resp) {
                        console.log("AGENT ID " + resp);
                        $("#household_id").val(resp.household_id);
                        return;
                    }
                });
            }
        }
    });

    if (localStorage) {
        /*
        local_provinces = localStorage.getItem("provinces");
        try {
            const provinces = JSON.parse(local_provinces);
            if (provinces["localProvinces"].length > 0) {
                for (var i=0; i<provinces["localProvinces"].length; i++) {
                    option_name =  provinces["localProvinces"][i].option_name;
                    option_value = provinces["localProvinces"][i].option_value;
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#select_province");
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#birth_province");
                }
                $('#select_province').selectmenu();
                $('#select_province').selectmenu('refresh', true);
                $('#birth_province').selectmenu();
                $('#birth_province').selectmenu('refresh', true);
            }
            else {
                var provincesArr = [];
                $.get(Census.Settings.provincesUrl,
                        function(data) {
                            for (var i=0; i<data.length; i++) {
                                option_name = data[i].name;
                                option_value = data[i].pk.toString();
                                var provinceObj = {option_name: option_name,
                                                    option_value: option_value};
                                provincesArr[i] = provinceObj;
                                $("<option/>").attr("value", option_value).text(option_name).appendTo("#select_province");
                                $("<option/>").attr("value", option_value).text(option_name).appendTo("#birth_province");
                            }
                            $('#select_province').selectmenu();
                            $('#select_province').selectmenu('refresh', true);
                            $('#birth_province').selectmenu();
                            $('#birth_province').selectmenu('refresh', true);
                            const provinces = {
                                localProvinces: provincesArr
                            }
                            const json = JSON.stringify(provinces);
                            localStorage.setItem("provinces", json);
                        });
            }
        }
        catch(err) {
            console.log(err.message);
            const provinces = "";
        }
        */
        /*
        local_head_household_links = localStorage.getItem("head_household_links");
        try {
            var head_household_links = JSON.parse(local_head_household_links);
        }
        catch(err){
            console.log(err.message);
            var head_household_links = "";
        }
        */
        /*
        if (!head_household_links) {
            var head_household_links_arr = [];
            $.get(Census.Settings.headHouseholdLinksUrl,
                function(data) {
                    console.log("HEAD LINKS SUCCESS");
                    console.log(data);
                    for (var i=0; i<data.length; i++) {
                        option_name = data[i].name;
                        option_value = data[i].pk.toString();
                        var head_link_obj = {option_name: option_name,
                                            option_value: option_value}
                        head_household_links_arr[i] = head_link_obj;
                    }
                    const head_household_links = {
                        local_head_household_links: head_household_links_arr
                    }
                    const head_json = JSON.stringify(head_household_links);
                    localStorage.setItem("local_head_household_links", head_json);
                });
        }
        */
    }
    
    CensusHouseholdRecord.get_provinces_choices("select_province");

    CensusHouseholdRecord.get_provinces_choices("birth_province");

    // Set head household links choices for the first resident
    ResidentRecord.get_head_household_link_choices("");

    // Set marrital status codes choices
    ResidentRecord.get_marrital_status_choices("");

    // Set marrital type choices
    ResidentRecord.get_marrital_type_choices("");

    // Set highest diploma choices
    ResidentRecord.get_highest_diploma_choices("");

    // Set occupation status choices
    ResidentRecord.get_occupation_status_choices("");

    // Set occupation situation choices
    ResidentRecord.get_occupation_situation_choices("");

    // Set religion choices
    ResidentRecord.get_religion_choices("");

    // Set handicap choices
    ResidentRecord.get_handicap_choices("");

    $(document).on("click", ".more_resident", function(ev) {
        ev.preventDefault();
        console.log("IN NEW RESIDENT INFO");
        var resident_list = $("form").find(".resident_info");
        var ind = resident_list.length;
        ind++;
        console.log("INDICE "+ ind);
        ind = ind.toString();
        var res_html = ResidentRecord.get_record_html(ind);
        //console.log(res_html);
        $("form").append(res_html);
        $.mobile.navigate("#household_resident-"+ind);
        if (parseInt(ind) > 1) {
            console.log("CREATE HOUSEHOLD OPTIONS " + ind);
            ResidentRecord.get_head_household_link_choices(ind);
            ResidentRecord.get_marrital_status_choices(ind);
            ResidentRecord.get_marrital_type_choices(ind);
            ResidentRecord.get_highest_diploma_choices(ind);
            ResidentRecord.get_occupation_status_choices(ind);
            ResidentRecord.get_occupation_situation_choices(ind);
            ResidentRecord.get_religion_choices(ind);
            ResidentRecord.get_handicap_choices(ind);
        }
    });
    
    /* Set head household links choices for additional residents
    $(".resident_info").on("pagecreate", function(event, ui) {
            var this_id = $(this).attr("id");
            console.log("RESIDENT CREATE THIS ID " + this_id);
            var id_parts = this_id.split("-");
            if (id_parts.length > 1) {
                console.log("INDEX "+id_parts[1]);
                ResidentRecord.get_head_household_link_choices(id_parts[1]);
            }
        });
    */

    $("input[name=zone_type]").click(function(e) {
        var value = $("input[name=zone_type]:checked").val();
        
        if (value == "zone_type_rural") {
            console.log("CLICKED " + value);
            $("#div_birth_city").addClass("bi-invisible");
            $("#div_birth_commune").addClass("bi-invisible");
            $("#div_birth_territory").removeClass("bi-invisible");
        }
        else if (value == "zone_type_urban") {
            console.log("CLICKED " + value);
            $("#div_birth_territory").addClass("bi-invisible");
            $("#div_birth_city").removeClass("bi-invisible");
            $("#div_birth_commune").removeClass("bi-invisible");
        }
    });
    /*
    $.get(Census.Settings.headHouseholdLinksUrl,
            function(data) {
                console.log("HEAD LINKS SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var head_link_obj = {option_name: option_name,
                                        option_value: option_value};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#head_household_link");
                }
                $("#head_household_link").selectmenu();
                $("#head_household_link").selectmenu("refresh", true);
            });
    
    $.get(Census.Settings.marritalStatusCodesUrl,
            function(data) {
                console.log("MARRITAL STATUS SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var marr_statut_obj = {option_name: option_name,
                                            option_value: option_value};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#marrital_status");
                    
                }
                $("#marrital_status").selectmenu();
                $("#marrital_status").selectmenu("refresh", true);
            });
    
    $.get(Census.Settings.marriageTypeCodesUrl,
            function(data) {
                console.log("MARRITAL TYPE SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var marr_type_obj = {option_name: option_name,
                                        option_value: option_value};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#marriage_type");
                }
                $("#marriage_type").selectmenu();
                $("#marriage_type").selectmenu("refresh", true);
            });
    $.get(Census.Settings.occupStatusCodesUrl,
            function(data) {
                console.log("OCCUPATION STATUS CODE");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var occ_stat_code = {option_value: option_value,
                                        option_name: option_name};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#occupation_status_code");
                }
                $("#occupation_status_code").selectmenu();
                $("#occupation_status_code").selectmenu("refresh", true);
            });
    $.get(Census.Settings.occupSituationCodesUrl,
            function(data) {
                console.log("OCCUPATION SITUATION CODE");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var occ_sit_code = {option_value: option_value,
                                        option_name: option_name};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#occupation_situation_code");
                }
                $("#occupation_situation_code").selectmenu();
                $("#occupation_situation_code").selectmenu("refresh", true);
            });
    $.get(Census.Settings.religionCodesUrl,
            function(data) {
                console.log("RELIGION CODES SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var rel_code = {option_value: option_value,
                                    option_name: option_name};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#religion");
                }
                $("#religion").selectmenu();
                $("#religion").selectmenu("refresh", true);
            });
    $.get(Census.Settings.handicapTypeCodesUrl,
            function(data) {
                console.log("HANDICAP CODES SUCCESS");
                console.log(data);
                for (var i=0; i<data.length; i++) {
                    option_name = data[i].name;
                    option_value = data[i].pk.toString();
                    var hand_code = {option_value: option_value,
                                    option_name: option_name};
                    $("<option/>").attr("value", option_value).text(option_name).appendTo("#handicap"); 
                }
                $("#handicap").selectmenu();
                $("#handicap").selectmenu("refresh", true);
            });
    */
});    
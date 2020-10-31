var ResidentRecord = ResidentRecord || {};
//Census.Settings = Census.Settings || {};

var elements_id = {
    "household_resident": "household_resident_",
    "first_name": "first_name_",
    "last_name": "last_name_",
    "head_household_link": "head_household_link_",
    "marrital_status": "marrital_status_",
    "marriage_type": "marriage_type_",
    "birth_date_day": "birth_date_day_",
    "birth_date_month": "birth_date_month_",
    "birth_date_year": "birth_date_year_",
    "resident_age": "resident_age_",
    "zone_type": "zone_type_",
    "zone_type_urban": "zone_type_urban_",
    "zone_type_rural": "zone_type_rural_",
    "div_birth_province": "div_birth_province_",
    "birth_province": "birth_province_",
    "birth_territory": "birth_territory_",
    "birth_city": "birth_city_",
    "birth_commune": "birth_commune_",
    "highest_diploma": "highest_diploma_",
    "occupation_status_code": "occupation_status_code_",
    "occupation_situation_code": "occupation_situation_code_",
    "occupation": "occupation_",
    "religion": "religion_",
    "handicap": "handicap_"
};
var index = 1;

ResidentRecord.get_record_html = function(indice) {
        var record_html = `
            <div data-role="page" id="household_resident-${indice}" class="a-page resident_info">
                <div data-role="header" data-theme="c">
                    <a href="" data-icon="carat-l">Retour</a>
                        <h1>R.D.C. Recensement</h1>
                    <a href="" data-icon="info">Contact</a>
                </div>
                <div role="main" class="ui-content">
                    <h2>R&eacute;sidents du M&eacute;nage</h2>
                    <h4>Personne ${indice}</h4>
                    <div data-role="fieldcontain">
                        <label for="first_name-${indice}">Pr&eacute;nom:</label>
                        <input type="text" name="first_name-${indice}" id="first_name-${indice}" value="" />
                    </div>
                    <div data-role="fieldcontain">
                        <label for="last_name-${indice}">Nom:</label>
                        <input type="text" name="last_name-${indice}" id="last_name-${indice}" value="" />
                    </div>
                    <div data-role="fieldcontain">
                        <label for="head_household_link-${indice}">Lien avec le Chef de M&eacute;nage:</label>
                        <select name="head_household_link-${indice}" id="head_household_link-${indice}" class="head_link" data-native-menu="false">
                            <option>Choisissez le lien avec le Chef de M&eacute;nage </option>
                        </select>
                    </div>
                    <div data-role="fieldcontain">
                        <label for="marrital_status-${indice}">Statut matrimonial:</label>
                        <select name="marrital_status-${indice}" id="marrital_status-${indice}" class="marr_status" data-native-menu="false">
                            <option>Choisissez le statut matrimonial</option>
                        </select>
                    </div>
                    <div data-role="fieldcontain">
                        <label for="marriage_type-${indice}">Type de mariage:</label>
                        <select name="marriage_type-${indice}" id="marriage_type-${indice}" class="marr_type" data-native-menu="false">
                            <option>Choisissez le type de mariage</option>
                        </select>
                    </div>
                    <p>
                        Date de Naissance:
                        <div class="ui-grid-a">
                            <div class="ui-block-a">
                                <fieldset data-role="controlgroup" data-type="horizontal">
                                    <legend>Date:</legend>
                                    <label for="birth_date_day-${indice}">Jour</label>
                                    <select name="birth_date_day-${indice}" id="birth_date_day-${indice}">
                                        <option>Jour</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                        <option value="6">6</option>
                                        <option value="7">7</option>
                                        <option value="8">8</option>
                                        <option value="9">9</option>
                                        <option value="10">10</option>
                                        <option value="11">11</option>
                                        <option value="12">12</option>
                                        <option value="13">13</option>
                                        <option value="14">14</option>
                                        <option value="15">15</option>
                                        <option value="16">16</option>
                                        <option value="17">17</option>
                                        <option value="18">18</option>
                                        <option value="19">19</option>
                                        <option value="20">20</option>
                                        <option value="21">21</option>
                                        <option value="22">22</option>
                                        <option value="23">23</option>
                                        <option value="24">24</option>
                                        <option value="25">25</option>
                                        <option value="26">26</option>
                                        <option value="27">27</option>
                                        <option value="28">28</option>
                                        <option value="29">29</option>
                                        <option value="30">30</option>
                                        <option value="31">31</option>
                                    </select>
                                    <label for="birth_date_month-${indice}">Mois</label>
                                    <select name="birth_date_month-${indice}" id="birth_date_month-${indice}">
                                        <option>Janvier</option>
                                        <option>F&eacute;vrier</option>
                                        <option>Mars</option>
                                        <option>Avril</option>
                                        <option>Mai</option>
                                        <option>Juin</option>
                                        <option>Juillet</option>
                                        <option>Ao&ucirc;t</option>
                                        <option>Septembre</option>
                                        <option>Octobre</option>
                                        <option>Novembre</option>
                                        <option>D&eacute;cembre</option>
                                    </select>
                                    <label for="birth_date_year-${indice}">Ann&eacute;e</label>
                                    <select name="birth_date_year-${indice}" id="birth_date_year-${indice}">
                                        <option>Ann&eacute;e</option>
                                        <option>2021</option>
                                        <option>2022</option>
                                    </select>
                                </fieldset>
                            </div>
                            <div class="ui-block-b">
                                <label for="resident_age-${indice}">
                                    Age:
                                </label>
                                <input type="text" name="resident_age-${indice}" id="resident_age-${indice}" value="" />
                            </div>
                        </div>
                    </p>
                    <p>
                        Lieu de Naissance
                        <div class="ui-grid-a">
                            <div class="ui-block-a">
                                <div data-role="fieldcontain">
                                    <fieldset data-role="controlgroup"data-type="horizontal" >
                                        <input type="radio" name="zone_type-${indice}" id="zone_type_urban-${indice}" value="zone_type_urban" checked="checked" />
                                        <label for="zone_type_urban-${indice}">Urbaine</label>
                                        <input type="radio" name="zone_type-${indice}" id="zone_type_rural-${indice}" value="zone_type_rural" />
                                        <label for="zone_type_rural-${indice}">Rurale</label>
                                    </fieldset>
                                </div>
                            </div>
                            <div class="ui-block-b">
                                <fieldset data-role="controlgroup">
                                    <div id="div_birth_province-${indice}">
                                        <select name="birth_province-${indice}" id="birth_province-${indice}" data-native-menu="false">
                                            <option>Choisissez la province</option>
                                        </select>
                                    </div>
                                    <div id="div_birth_territory-${indice}" class="bi-invisible">
                                        <select name="birth_territory-${indice}" class="smallest_unit" id="birth_territory-${indice}" data-native-menu="false">
                                            <option>Choisissez le territoire</option>
                                        </select>
                                    </div>
                                    <div id="div_birth_city-${indice}">
                                        <select name="birth_city-${indice}" id="birth_city-${indice}" data-native-menu="false">
                                            <option>Choisissez la ville</option>
                                        </select>
                                    </div>
                                    <div id="div_birth_commune-${indice}">
                                        <select name="birth_commune-${indice}" class="smallest_unit" id="birth_commune-${indice}" data-native-menu="false">
                                            <option>Choisissez la commune</option>
                                        </select>
                                   </div>
                                </fieldset>
                            </div>
                        </div>
                    </p>
                    <div data-role="fieldcontain">
                        <label for="highest_diploma-${indice}">Plus haut dipl&ocirc;me obtenu:</label>
                        <select name="highest_diploma-${indice}" id="highest_diploma-${indice}" data-native-menu="false">
                            <option>Choisissez le dipl&ocirc;me</option>
                        </select>
                    </div>
                    <div data-role="fieldcontain">
                        <label for="occupation_status-${indice}">Status de l'emploi:</label>
                        <select name="occupation_status-${indice}" id="occupation_status-${indice}" data-native-menu="false">
                            <option>Choisissez le status de l'emploi</option>
                        </select>
                    </div>
                    <div data-role="fieldcontain">
                        <label for="occupation_situation-${indice}">Situation de l'emploi:</label>
                        <select name="occupation_situation-${indice}" id="occupation_situation-${indice}" data-native-menu="false">
                            <option>Choisissez la situation de l'emploi</option>
                        </select>
                    </div>
                    <div data-role="fieldcontain">
                        <label for="occupation-${indice}">Occupation:</label>
                        <input type="text" name="occupation-${indice}" id="occupation-${indice}" value="" />
                    </div>
                    <div data-role="fieldcontain">
                        <label for="religion-${indice}">Religion:</label>
                        <select name="religion-${indice}" id="religion-${indice}" data-native-menu="false">
                            <option>Choisissez la religion</option>
                        </select>
                    </div>
                    <div data-role="fieldcontain">
                        <label for="handicap-${indice}">Type de l'handicap:</label>
                        <select name="handicap-${indice}" id="handicap-${indice}" data-native-menu="false">
                        $(el_selector).selectmenu();
                        $(el_selector).selectmenu("refresh", true);                    <option>Choisissez le type d'handicap</option>
                        </select>
                    </div>
                    <p>
                        <div class="ui-grid-a">
                            <div class="ui-block-a">
                                <a data-role="button" href="">
                                    Sauvez partiellement
                                </a>
                            </div>
                            <div class="ui-block-b">
                                <a data-role="button" class="more_resident" href="#household_resident-${indice+1}">
                                    Continue
                                </a>
                            </div>
                        </div>
                    </p>
                </div>
                <div data-role="footer">
                    <h4>Copyright Fonsdom &copy; 2020</h4>
                </div>
            </div>`;
        return record_html;    
}

ResidentRecord.get_head_household_link_choices = function(ind) {
    let send_request = false;
    local_head_household_links = localStorage.getItem("local_head_household_links");
    if (local_head_household_links === null) {
        send_request = true;
    }
    let head_household_links = "";
    if (ind) {
        var el_selector = "#head_household_link-" + ind;
    }
    else {
        var el_selector = "#head_household_link";
    }
    try {
        if (!send_request) {
            head_household_links = JSON.parse(local_head_household_links);
            console.log(head_household_links);
            if (head_household_links.local_head_household_links === undefined ||
                    head_household_links["local_head_household_links"].length < 1) {
                send_request = true;
            } 
        }
        if (send_request) {
            var head_household_link_arr = [];
            $.get(Census.Settings.headHouseholdLinksUrl,
                function(data) {
                    if (data) {
                        console.log("HEAD LINKS SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var head_household_link_obj = {option_name: option_name,
                                                            option_value: option_value};
                            head_household_link_arr[i] = head_household_link_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);
                        }
                        $(el_selector).selectmenu();
                        $(el_selector).selectmenu("refresh", true);
                        const head_household_link_storage = {
                            local_head_household_links: head_household_link_arr
                        };
                        const head_household_link_json = JSON.stringify(head_household_link_storage);
                        localStorage.setItem("local_head_household_links", head_household_link_json);   
                    }
                    
                });  
        }
        else {
            head_household_links = head_household_links["local_head_household_links"];
            for (var i=0; i<head_household_links.length; i++) {
                console.log("HEAD_HOUSEHOLD_LINK STATUS EXISTS HERE");
                var option_name = head_household_links[i].option_name;
                var option_value = head_household_links[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        head_household_links = "";
    }
}

ResidentRecord.get_marrital_status_choices = function(ind) {
    let send_request = false;
    var local_marrital_status = localStorage.getItem("local_marrital_status");
    if (local_marrital_status === null) {
        send_request = true;
    }
    let marrital_status = "";
    if (ind) {
        var el_selector = "#marrital_status-" + ind;
    }
    else {
        var el_selector = "#marrital_status";
    }
    try {
        if (!send_request) {
            marrital_status = JSON.parse(local_marrital_status);
            console.log(marrital_status);
            if (marrital_status.local_marrital_status === undefined || 
                        marrital_status["local_marrital_status"].length > 0) {
                send_request = true;
            }
        }
        if (send_request) {
            var marrital_status_arr = [];
            $.get(Census.Settings.marritalStatusCodesUrl,
                function(data) {
                    if (data) {
                        console.log("MARRITAL STATUS SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var marr_statut_obj = {option_name: option_name,
                                                    option_value: option_value};
                            marrital_status_arr[i] = marr_statut_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);
                        }
                        $(el_selector).selectmenu();
                        $(el_selector).selectmenu("refresh", true);
                        const marrital_status_storage = {
                            local_marrital_status: marrital_status_arr
                        };
                        const marrital_status_json  = JSON.stringify(marrital_status_storage);
                        localStorage.setItem("local_marrital_status", marrital_status_json);
                    }
                });
        }
        else {
            marrital_status = marrital_status["local_marrital_status"];
            for (var i=0; i<marrital_status.length; i++) {
                console.log("MARRITAL STATUS EXISTS HERE");
                var option_name = marrital_status[i].option_name;
                var option_value = marrital_status[i].option_value;
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

ResidentRecord.get_marrital_type_choices = function(ind) {
    let send_request = false;
    var local_marrital_type = localStorage.getItem("local_marrital_type");
    if (local_marrital_type === null) {
        send_request = true;
    }
    let_marrital_type = "";
    if (ind) {
        var el_selector = "#marrital_type-" + ind;
    }
    else {
        var el_selector = "#marrital_type";
    }
    try {
        if (!send_request) {
            marrital_type = JSON.parse(local_marrital_type);
            console.log(marrital_type);
            if (marrital_type.local_marrital_type === undefined || 
                        marrital_type["local_marrital_type"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var marrital_type_arr = [];
            $.get(Census.Settings.marriageTypeCodesUrl,
                function(data) {
                    if (data) {
                        console.log("MARRITAL TYPE SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var marr_type_obj = {option_name: option_name,
                                                option_value: option_value};
                            marrital_type_arr[i] = marr_type_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
                        }
                        $(el_selector).selectmenu();
                        $(el_selector).selectmenu("refresh", true);
                        const marrital_type_storage = {
                            local_marrital_type: marrital_type_arr
                        };
                        const marrital_type_json = JSON.stringify(marrital_type_storage);
                        localStorage.setItem("local_marrital_type", marrital_type_json);
                    }
                });
        }
        else {
            marrital_type = marrital_type["local_marrital_type"];
            for (var i=0; i<marrital_type.length; i++) {
                console.log("MARRITAL TYPE EXISTS HERE");
                var option_name = marrital_type[i].option_name;
                var option_value = marrital_type[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        marrital_type = "";
    }
};

ResidentRecord.get_highest_diploma_choices = function(ind) {
    let send_request = false;
    var local_highest_diploma = localStorage.getItem("local_highest_diploma");
    if (local_highest_diploma === null) {
        send_request = true;
    }
    let highest_diploma = "";
    if (ind) {
        var el_selector = "#highest_diploma-" + ind;
    }
    else {
        var el_selector = "#highest_diploma";
    }
    try {
        if (!send_request) {
            highest_diploma = JSON.parse(local_highest_diploma);
            console.log(highest_diploma);
            if (highest_diploma.local_highest_diploma === undefined ||
                        highest_diploma["local_highest_diploma"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var highest_diploma_arr = [];
            $.get(Census.Settings.highestDiplomaCodesUrl,
                function(data) {
                    if (data) {
                        console.log("HIGHEST DIPLOMA SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var highest_diploma_obj = {option_name: option_name,
                                                        option_value: option_value};
                            highest_diploma_arr[i] = highest_diploma_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);     
                        }
                        const highest_diploma_storage = {
                            local_highest_diploma: highest_diploma_arr
                        };
                        const highest_diploma_json = JSON.stringify(highest_diploma_storage);
                        localStorage.setItem("local_highest_diploma", highest_diploma_json);
                    }
                });
        }
        else {
            highest_diploma = highest_diploma["local_highest_diploma"];
            for (var i=0; i<highest_diploma.length; i++) {
                console.log("HIGHEST DIPLOMA EXISTS HERE");
                var option_name = highest_diploma[i].option_name;
                var option_value = highest_diploma[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        highest_diploma = "";
    }
};

ResidentRecord.get_occupation_status_choices = function (ind) {
    let send_request = false;
    var local_occupation_status = localStorage.getItem("local_occupation_status");
    if (local_occupation_status === null) {
        send_request = true;
    }
    let occupation_status = "";
    if (ind) {
        var el_selector = "#occupation_status-" + ind;
    }
    else {
        var el_selector = "#occupation_status";
    }
    try {
        if (!send_request) {
            occupation_status = JSON.parse(local_occupation_status);
            console.log(occupation_status);
            if (occupation_status.local_occupation_status === undefined ||
                        occupation_status["local_occupation_status"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var occupation_status_arr = [];
            $.get(Census.Settings.occupStatusCodesUrl,
                function(data) {
                    if (data) {
                        console.log("OCCUPATION STATUS SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var occupation_status_obj = {option_name: option_name,
                                                        option_value: option_value};
                            occupation_status_arr[i] = occupation_status_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector);
                        }
                        const occupation_status_storage = {
                            local_occupation_status: occupation_status_arr
                        };
                        const occupation_status_json = JSON.stringify(occupation_status_storage);
                        localStorage.setItem("local_occupation_status", occupation_status_json);
                    }
                });
        }
        else {
            occupation_status = occupation_status["local_occupation_status"];
            for (var i=0; i<occupation_status.length; i++) {
                console.log("OCCUPATION STATUS EXISTS HERE");
                var option_name = occupation_status[i].option_name;
                var option_value = occupation_status[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
            }$(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        occupation_status = "";
    }
};

ResidentRecord.get_occupation_situation_choices = function (ind) {
    let send_request = false;
    var local_occupation_situation = localStorage.getItem("local_occupation_situation");
    if (local_occupation_situation === null) {
       send_request = true;
    }
    let occupation_situation = "";
    if (ind) {
       var el_selector = "#occupation_situation-" + ind;
    }
    else {
        var el_selector = "#occupation_situation";
    }
    try {
        if (!send_request) {
            occupation_situation = JSON.parse(local_occupation_situation);
            console.log(occupation_situation);
            if (occupation_situation.local_occupation_situation === undefined ||
                        occupation_situation["local_occupation_situation"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var occupation_situation_arr = [];
            $.get(Census.Settings.occupSituationCodesUrl,
                function(data) {
                    if (data) {
                        console.log("OCCUPATION SITUATION SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var occupation_situation_obj = {option_name: option_name,
                                                            option_value: option_value};
                            occupation_situation_arr[i] = occupation_situation_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
                        }
                        const occupation_situation_storage = {
                            local_occupation_situation: occupation_situation_arr
                        };
                        const occupation_situation_json = JSON.stringify(occupation_situation_storage);
                        localStorage.setItem("local_occupation_situation", occupation_situation_json);
                    }
                });
        }
        else {
            occupation_situation = occupation_situation["local_occupation_situation"];
            for (var i=0; i<occupation_situation.length; i++) {
                console.log("OCCUPATION_SITUATION EXISTS HERE");
                var option_name = marrital_status[i].option_name;
                var option_value = marrital_status[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector) 
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        occupation_situation = "";
    } 
};

ResidentRecord.get_religion_choices = function (ind) {
    let send_request = false;
    var local_religion = localStorage.getItem("religion");
    if (local_religion === null) {
        send_request = true;
    }
    let religion = "";
    if (ind) {
        var el_selector = "#religion-" + ind;
    }
    else {
        var el_selector = "#religion";
    }
    try {
        if (!send_request) {
            religion = JSON.parse(local_religion);
            console.log(religion);
            if (religion.local_religion === undefined || 
                            religion["local_religion"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var religion_arr = [];
            $.get(Census.Settings.religionCodesUrl,
                function(data) {
                    if (data) {
                        console.log("RELIGION SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var religion_obj = {option_name: option_name,
                                                option_value: option_value};
                            religion_arr[i] = religion_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
                        }
                        const religion_storage = {
                            local_religion: religion_arr
                        };
                        const religion_json = JSON.stringify(religion_storage);
                        localStorage.setItem("local_religion", religion_json);
                    }
                });
        }
        else {
            religion = religion["local_religion"];
            for (var i=0; i<religion.length; i++) {
                console.log("RELIGION EXISTS HERE");
                var option_name = religion[i].option_name;
                var option_value = religion[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        religion = "";
    }    
};

ResidentRecord.get_handicap_choices = function (ind) {
    let send_request = false;
    var local_handicap = localStorage.getItem("local_handicap");
    if (local_handicap === null) {
        send_request = true;
    }
    let handicap = "";
    if (ind) {
        var el_selector = "#handicap-" + ind;
    }
    else {
        var el_selector = "#handicap";
    }
    try {
        if (!send_request) {
            handicap = JSON.parse(local_handicap);
            console.log(handicap);
            if (handicap.local_handicap === undefined ||
                        handicap["local_handicap"].length < 1) {
                send_request = true;
            }
        }
        if (send_request) {
            var handicap_arr = [];
            $.get(Census.Settings.handicapTypeCodesUrl,
                function(data) {
                    if (data) {
                        console.log("HANDICAP SUCCESS");
                        console.log(data);
                        for (var i=0; i<data.length; i++) {
                            option_name = data[i].name;
                            option_value = data[i].pk.toString();
                            var handicap_obj = {option_name: option_name,
                                                option_value: option_value};
                            handicap_arr[i] = handicap_obj;
                            $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
                        }
                        const handicap_storage = {
                            local_handicap: handicap_arr
                        }
                        const handicap_json = JSON.stringify(handicap_storage);
                        localStorage.setItem("local_handicap", handicap_json);
                    }
                });
        }
        else {
            handicap = handicap["local_handicap"];
            for (var i=0; i<handicap.length; i++) {
                console.log("HANDICAP EXISTS HERE");
                var option_name = handicap[i].option_name;
                var option_value = handicap[i].option_value;
                $("<option/>").attr("value", option_value).text(option_name).appendTo(el_selector); 
            }
            $(el_selector).selectmenu();
            $(el_selector).selectmenu("refresh", true);
        }
    }
    catch (err) {
        console.log(err.message);
        handicap = "";
    }  
};
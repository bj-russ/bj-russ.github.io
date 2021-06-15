function update_page_variables(variables_to_update, options, update_controls = false) {
    var variables_to_update_dict = {};
    for (var index = 0; index < variables_to_update.length; index++) {  // build dict object of {name: value}, to send to server. (Here, value = name)
        variables_to_update_dict[variables_to_update[index]] = variables_to_update[index];
    };
    $.ajax({                                                           // ajax 'get' request to server.
        url: $SCRIPT_ROOT + "/_update_page_variables",
        type: "GET",
        data: variables_to_update_dict,
        success: function (response) {                                   // parse response from server
            var updated_variables = response.ajax_data;
            console.log(updated_variables);
            updated_variables = update_options(updated_variables, options); // Check if variables have options and apply changes
            for (var i in updated_variables) {                         // Loop through response and update each variable
                updated_variable = updated_variables[i];
                $('#' + i).html(updated_variable);               // update value at current id
                $('#' + i).addClass('bold');                    // bold numbers when they are updated
                if (update_controls == true) {                       // case for updating control setting. 
                    var type = $("#input_" + i).attr('type');       // check input type
                    if (type == 'checkbox') {                        // if checkbox set checked to current value
                        console.log(updated_variable)
                        if (updated_variable == 1 || updated_variable == "On" || updated_variable == "true" | updated_variable == "on" || updated_variable == "1") {
                            document.getElementById('input_' + i).checked = true;
                        } else {
                            document.getElementById('input_' + i).checked = false;
                        }
                    }
                }
                //changeBackgroundColor("#" + i, number_received);// change background color based on value for alarming reasons
            }
            
            return updated_variables
        }

    })

}

// this function is used to check if the variable has a special option and applies the option. Currently converts 1/0 to On/Off. 
function update_options(variables, options) {
    var updated_variables = {}
    for (i in variables) {
        variable = variables[i]
        if (i in options) {                              // check if variable has option
            if (options[i] == 'onOff') {                  // check if option is onOff and replace 1/0 with On/Off
                if (variable == 1 || variable == true || variable == 'true' || variable == 'True' || variable == "on" || variable == "On" || variable == "ON") {
                    variable = 'On';
                } else {
                    variable = 'Off';
                }

            }
        }
        if (options[i] == 'alarm') {
            if (variable == 1) {
                variable = "ALARM!";
                document.getElementById(i).style.backgroundColor = "red";

            }
            if (variable == 0) {
                variable = "OK!"
                document.getElementById(i).style.backgroundColor = "lightgreen";
            }
            else {
                variable = "N/A"
                document.getElementById(related_ele).style.backgroundColor = "transparent";
                document.getElementById(i).style.backgroundColor = "transparent";
            }
        }
        if (options[i] == 'warning') {
            var related_ele = i.slice(8); // get related element for setting up background coloour of element
            if (variable == 1) {
                variable = "Warning!";
                document.getElementById(i).style.backgroundColor = "gold";
                document.getElementById(related_ele).style.backgroundColor = "gold";
            } else if (variable == 0) {
                variable = "In Range!"
                document.getElementById(related_ele).style.backgroundColor = "lightgreen";
                document.getElementById(i).style.backgroundColor = "lightgreen";
            } else {
                variable = "N/A"
                document.getElementById(related_ele).style.backgroundColor = "transparent";
                document.getElementById(i).style.backgroundColor = "transparent";
            }
        }
        if (options[i] == "trafficlight") {
            var shed_rel = i.slice(13);
            clear(shed_rel)
            if (variable == "on") {
                variable = "SHED On"
                document.getElementById(shed_rel + "_green").className = "light green";
            }
            else if (variable == "out_of_range") {
                variable = "Out of Range"
                document.getElementById(shed_rel + "_amber").className = "light amber";
            }
            else if (variable == "off") {
                variable = "Off"
                document.getElementById(shed_rel + "_red").className = "light red";
            }
            else if (variable == "alarm") {
                variable = "ALARM!"
                document.getElementById(shed_rel + "_red").className = "light red";
                document.getElementById(shed_rel + "_amber").className = "light amber";
            }
            else {
                clear(shed_rel)
            }
        }
        if (options[i] == "TEMPERATURE") {
            variable = String(variable) + " &degC";
        }
        if (options[i] == "GPM") {

            variable = String(variable) + "\n GPM";
        }
        updated_variables[i] = variable
    }
    return updated_variables
}
// This function is used to set variable values in the server
function set_variable_value(variable_to_set) {
    $.ajax({                                                    // Ajax request to send data to server
        type: "GET",
        url: "_set_variable_value",                             // Route address for changing variable values
        data: variable_to_set,
        success: function (response) {                            // log to console on successful response
            console.log(response)
        },
    })
}

// Runs on button clicks. Checks the current variable value using an indicator, toggles the state and calls set_variable_value to update the variable in the server
// example html usage -> <button type="button" onclick="buttonClicked('variable_name')">Variable Name</button>
function buttonClicked(variable_id) {
    var variable_value_current = $('#' + variable_id).text(); // text is used for getting the html string between the tag brackets. Val works on input boxes.
    var variable_value_new = 0
    if ((variable_value_current == 0) || (variable_value_current == 'Off') || variable_value_current == 'false' || variable_value_current == 'off' || variable_value_current == false) {       // check the current state and update with new value, case added for onOff option
        variable_value_new = 1
    } else {
        variable_value_new = 0
    }
    var variable = {}
    variable[variable_id] = variable_value_new
    set_variable_value(variable)                                                    // send new setting to server.
}

//Button click for alarm reset.
function buttonAlarm(variable_id) {
    var variable = variable_id.slice(6)
    $.ajax({                                                    // Ajax request to send data to server
        type: "GET",
        url: "_alarm_reset",                             // Route address for changing variable values
        data: variable,
        success: function (response) {                            // log to console on successful response
            console.log(response)
        },
    })

}


// Initializes options list. Checks for _onOff suffix on tag id, removes from id and stores variable name in option list. For use on update to change 1/0 to on/off. -> call before get_variables
function check_ID_Options(allIDs) {
    //var allIDs = document.querySelectorAll('[id]');             // get IDs from html
    var options = {};                                           // initialize options list
    for (var i = 0; i < allIDs.length; i++) {                    // loop through list of IDs
        var id = allIDs[i].id;                                  // get current id
        if (id.includes('_onOff')) {                             // check if id includes option onOff
            var new_id = id.replace("_onOff", "");              // replace option with blank and save new id
            document.getElementById(id).id = new_id;            // replace original id with new id
            options[new_id] = 'onOff';                           // add to options object for future use
        }
        if (id.includes('alarm_')) {
            var new_id = id.replace("", "");
            document.getElementById(id).id = new_id;
            options[id] = 'alarm';
        }
        if (id.includes('warning_')) {
            var new_id = id.replace("", "");
            document.getElementById(id).id = new_id;
            options[id] = 'warning';
        }
        if (id.includes('trafficlight_')) {
            var new_id = id.replace("", "");
            document.getElementById(id).id = new_id;
            options[id] = 'trafficlight';
        }
        if (!id.includes("warning_") & !id.includes("_onOff") && !id.includes('alarm_')) {
            if (id.includes("Flowmeter")) {
                var new_id = id.replace("", "");
                document.getElementById(id).id = new_id;
                options[id] = 'GPM';
            }
            if (id.includes("T_")) {
                var new_id = id.replace("", "");
                document.getElementById(id).id = new_id;
                options[id] = 'TEMPERATURE';
            }
        }
    }
    //console.log(options)
    return options
}

// Change the background color based on the temperature value, could use range parameter for each value. eg, get info from config file on server for each variable, alarm enabled, alarm status, range high, range low.
function changeBackgroundColor(input, value) {
    $().removeClass();
    if (value < 15) {
        $(input).addClass('range_low bold');
    }
    else if (value >= 15 && value <= 25) {
        $(input).addClass('range_normal bold');
    }
    else {
        $(input).addClass('range_high bold');
    }
}

// get page variables and separate into indicators and controls (inputs and outputs). Builds list of variables for use in monitoring for changes and updating
function get_variables() {
    var allVariables = document.querySelectorAll('[id]');               // get all id names from html
    var options = check_ID_Options(allVariables);                       // check if id has associated option
    //console.log(allVariables)
    var inputs = [];
    var outputs = [];
    for (var index = 0; index < allVariables.length; index++) {          // iterate through list, separating inputs and removing the input_tag from the names
        var variable = allVariables[index].id;
        if (variable.includes('input_')) {
            var input = variable.replace("input_", "");
            inputs.push(input);
        } else {
            outputs.push(variable);
        }
    }
    var variables = { "Inputs": inputs, "Outputs": outputs }              // return object {dict} of input and output names
    return [variables, options];
}

// create string of input names to watch in .change function. Uses the format for jquery of #input_id, etc. This is used as the actual string that JQuery uses to monitor for changes to controls
function generate_input_string(Inputs) {
    var input_string = "";
    for (var i = 0; i < Inputs.length; i++) {                            // build JQuery string for each variable. Uses the format "#input_variableName, ". The string will have all of the variables separated by commas.i
        var str1 = "#";
        var str2 = "input_";
        var str3 = Inputs[i];
        var str4 = ", "
        input_string = input_string.concat(str1, str2, str3, str4);
    }
    input_string = input_string.slice(0, -2);                           // removes trailing ", " from the end of the string.
    return input_string
}

// get initial list of inputs and store their values. This is used for checking when controls are changed. Inputs are compared to their previous values and sent to server when they are changed.
// This could grab the values from the server and update the display instead
function get_input_values(Inputs) {                              // gets the current settings from all id's with prefix input_, currently working for checkbox and numeric, add others as needed.
    var input_values = {}
    for (var i = 0; i < Inputs.length; i++) {
        var type = $("#input_" + Inputs[i]).attr('type');       // check input type
        if (type == 'checkbox') {
            input_values[Inputs[i]] = $("#input_" + Inputs[i]).prop('checked');
        }
        else {
            input_values[Inputs[i]] = $("#input_" + Inputs[i]).val()
        }
    }
    console.log(input_values)
    return input_values
}

// Initializes the input values from the server when the page loads.
function initialize_input_values(Inputs, options) {
    // get input variables. Get values from server. Push values to page. Store in input_values for future use.
    update_page_variables(Inputs, options, true)

}

// clear function for trafficlight
function clear(shed_rel) {
    document.getElementById(shed_rel + "_red").className = "light off";
    document.getElementById(shed_rel + "_amber").className = "light off";
    document.getElementById(shed_rel + "_green").className = "light off";
}


//Runs once the document is ready and published in the browser.
$(document).ready(function () {

    // update navbar with indicator of current page (currently color, can increase font etc.)
    $("[href]").each(function () {
        if (this.href == window.location.href) {
            $(this).addClass("currentLink");
        }
    });

    //This is used for https transfers when deployed to online server
    // var socket = io.connect('https://' + document.domain + ':' + location.port + '/test', {secure: true});

    //This is used for http transfers when deployed to local network
    // var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    // get list of variables used by page (tags which have and id="")
    var variables_options = get_variables()                         // Get page variables and their associated options
    var variables = variables_options[0]                            // Create list of page variables
    var options = variables_options[1]                              // Create list of variable options
    initialize_input_values(variables.Inputs, options)
    // Set JQuery refresh interval. This updates the page variables at the set frequency "1 Hz"
    setInterval(update_page_variables, 1000, variables.Outputs, options)

    // monitor inputs for changes, trying to use variables.Inputs to automatically work with changing html
    var input_string = generate_input_string(variables.Inputs)      // generate list of current inputs as a string to monitor for changes
    var inputs_prev = get_input_values(variables.Inputs)            // initialize list of current input values for tracking which input has changed


    $(input_string).on("change", function () {                        // monitor input string for changes, run on change
        var inputs_current = {}
        var input_changed = {}
        inputs_current = get_input_values(variables.Inputs)         // check current values for inputs
        for (var i = 0; i < variables.Inputs.length; i++) {
            var input = variables.Inputs[i];
            if (inputs_current[input] != inputs_prev[input]) {       // check if this input has changed from previous, if so add to list of changes to send to server and update list of previous readings for next evaluation
                inputs_prev[input] = inputs_current[input];
                input_changed[input] = inputs_current[input];
            }
        }
        set_variable_value(input_changed)                           // send new value to server
    })
    //connect the socket to the server.

    //This is used for https transfers when deployed to online server

    var ctx3 = document.getElementById('myChart_shed3').getContext('2d');
    
    var myChart_shed3 = new Chart(ctx3, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "SHED3 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 50,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                }, {
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 15,
                        fontColor: "#3e95cd"
                    },
                    id: 'B',
                    type: 'linear',
                    position: 'right',
                    scaleLabel: {
                        labelString: 'Valve Voltage [v]',
                        display: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        maxTicksLimit: 24,
                        maxRotation: 45,
                        minRotation: 45
                    },
                    scaleLabel: {
                        labelString: 'Time of day',
                        display: true
                    }
                }]
            },
            elements: {
                point: {
                    radius: 0
                }
            }
        }
    });
    
    //Update charge with data from server once received from ajax call
    function successinitialized(myChart, record_data) {
        myChart.data = {
            labels: record_data.time,
            datasets: [{
                data: record_data.temp,
                label: "Temperature [C]",
                borderColor: "#c45850",
                fill: false,
                yAxisID: 'A'
            }, {
                data: record_data.valve,
                label: "Valve [v]",
                borderColor: "#3e95cd",
                fill: false,
                yAxisID: 'B'
            }]
        }
        myChart.update();
        return myChart;
    };
    //asynchronous call to server for unitial chart data
    function initializedata_shed3(myChart) {
        $.ajax({
            url: "_initialize_data",
            type: "GET",
            success: function (response) {
                var temp_data = response.T_shed3;
                var valve_data = response.Valve_shed3_hot;
                var time_data = response.time;
                var record_data = { temp: temp_data, valve: valve_data, time: time_data };
                successinitialized(myChart, record_data); //update chart with data

            }
        });
    };


    //initiate the data retrieval process

    initializedata_shed3(myChart_shed3);
    setInterval(update_chart_shed3, 5000, myChart_shed3)  //300000 is updated every 5 minutes
    
    //update chart with data received.
    function update_chart_shed3(myChart) {
        $.ajax({
            url: "_update_data",
            type: "GET",
            success: function (response) {
                var temp_data = response.data.T_shed3;
                var valve_data = response.data.Valve_shed3_hot;
                var time_data = response.data.chart_time;
                var new_data = [temp_data, valve_data,time_data];


                console.log("Received new Chart Data: " +new_data +" with time stamp: " + time_data);
                console.log(response.data)
                if (myChart.data.labels.length >= 1000) {
                    myChart.data.labels.shift();
                    myChart.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })

                }
                myChart.data.labels.push(time_data);
                myChart.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data[index]);
                })
                myChart.update();
                
            }
        })
        

    };
    

})



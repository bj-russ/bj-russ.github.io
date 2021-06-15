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
        variable_value_new = true
    } else {
        variable_value_new = false
    }
    var variable = {}
    variable[variable_id] = variable_value_new
    set_variable_value(variable)                                                    // send new setting to server.
}
function initialize_input_values(Inputs, options) {
    // get input variables. Get values from server. Push values to page. Store in input_values for future use.
    update_page_variables(Inputs, options, true)


}

$(document).ready(function () {
    // update navbar with indicator of current page (currently color, can increase font etc.)
    $("[href]").each(function () {
        if (this.href == window.location.href) {
            $(this).addClass("currentLink");
        }
    });

    var ctx1 = document.getElementById('myChart_soak1').getContext('2d');
    var ctx2 = document.getElementById('myChart_soak2').getContext('2d');
    var ctx3 = document.getElementById('myChart_soak3').getContext('2d');
    var ctx4 = document.getElementById('myChart_soak4').getContext('2d');
    var ctx5 = document.getElementById('myChart_soak5').getContext('2d');
    var ctx6 = document.getElementById('myChart_soak6').getContext('2d');
    // var ctx7 = document.getElementById('myChart_soak7').getContext('2d');
    // var ctx8 = document.getElementById('myChart_soak8').getContext('2d');

    var myChart_soak1 = new Chart(ctx1, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "Area 1 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 35,
                        min: 10,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                },
                    // {
                    //     ticks: {
                    //         beginAtZero: true,
                    //         suggestedMax: 15,
                    //         fontColor: "#3e95cd"
                    //     },
                    // id: 'B',
                    // type: 'linear',
                    // position: 'right',
                    // scaleLabel: {
                    //     labelString: 'Valve Voltage [v]',
                    //     display: true
                    // }
                ],
                xAxes: [{
                    ticks: {
                        //maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 15
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

    var myChart_soak2 = new Chart(ctx2, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "Area 2 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 35,
                        suggestedMin: 15,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                },
                    // {
                    //     ticks: {
                    //         beginAtZero: true,
                    //         suggestedMax: 15,
                    //         fontColor: "#3e95cd"
                    //     },
                    // id: 'B',
                    // type: 'linear',
                    // position: 'right',
                    // scaleLabel: {
                    //     labelString: 'Valve Voltage [v]',
                    //     display: true
                    // }
                ],
                xAxes: [{
                    ticks: {
                        //maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 30
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
    var myChart_soak3 = new Chart(ctx3, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "Area 3 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 35,
                        suggestedMin: 15,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                },
                    // {
                    //     ticks: {
                    //         beginAtZero: true,
                    //         suggestedMax: 15,
                    //         fontColor: "#3e95cd"
                    //     },
                    // id: 'B',
                    // type: 'linear',
                    // position: 'right',
                    // scaleLabel: {
                    //     labelString: 'Valve Voltage [v]',
                    //     display: true
                    // }
                ],
                xAxes: [{
                    ticks: {
                        //maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 30
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
    var myChart_soak4 = new Chart(ctx4, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "Area 4 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 35,
                        suggestedMin: 15,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                },
                    // {
                    //     ticks: {
                    //         beginAtZero: true,
                    //         suggestedMax: 15,
                    //         fontColor: "#3e95cd"
                    //     },
                    // id: 'B',
                    // type: 'linear',
                    // position: 'right',
                    // scaleLabel: {
                    //     labelString: 'Valve Voltage [v]',
                    //     display: true
                    // }
                ],
                xAxes: [{
                    ticks: {
                        //maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 30
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
    var myChart_soak5 = new Chart(ctx5, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "Area 5 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 35,
                        suggestedMin: 15,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                },
                    // {
                    //     ticks: {
                    //         beginAtZero: true,
                    //         suggestedMax: 15,
                    //         fontColor: "#3e95cd"
                    //     },
                    // id: 'B',
                    // type: 'linear',
                    // position: 'right',
                    // scaleLabel: {
                    //     labelString: 'Valve Voltage [v]',
                    //     display: true
                    // }
                ],
                xAxes: [{
                    ticks: {
                        //maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 30
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
    var myChart_soak6 = new Chart(ctx6, {
        type: 'line',
        data: [],
        options: {
            title: {
                display: true,
                text: "Area 6 Temperature Record",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 35,
                        suggestedMin: 15,
                        fontColor: '#c45850'
                    },
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        labelString: 'Temperature [C]',
                        display: true
                    }
                },
                    // {
                    //     ticks: {
                    //         beginAtZero: true,
                    //         suggestedMax: 15,
                    //         fontColor: "#3e95cd"
                    //     },
                    // id: 'B',
                    // type: 'linear',
                    // position: 'right',
                    // scaleLabel: {
                    //     labelString: 'Valve Voltage [v]',
                    //     display: true
                    // }
                ],
                xAxes: [{
                    ticks: {
                        maxRotation: 30,
                        minRotation: 30,
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
            }//, {
                // data: record_data.valve,
                // label: "Valve [v]",
                // borderColor: "#3e95cd",
                // fill: false,
                // yAxisID: 'B'
                // }
            ]
        }
        myChart.update();
        return myChart;
    };
    //asynchronous call to server for unitial chart data
    function initializedata_soak(myChart1, myChart2, myChart3, myChart4, myChart5, myChart6, myChart7, myChart8) {
        $.ajax({
            url: "_initialize_data_soak",
            type: "GET",
            success: function (response) {
                var time_data = response.data.chart_time;

                var temp_data1 = response.data.T_soak1;
                var temp_data2 = response.data.T_soak2;
                var temp_data3 = response.data.T_soak3;
                var temp_data4 = response.data.T_soak4;
                var temp_data5 = response.data.T_soak5;
                var temp_data6 = response.data.T_soak6;

                var record_data1 = { temp: temp_data1, time: time_data };
                var record_data2 = { temp: temp_data2, time: time_data };
                var record_data3 = { temp: temp_data3, time: time_data };
                var record_data4 = { temp: temp_data4, time: time_data };
                var record_data5 = { temp: temp_data5, time: time_data };
                var record_data6 = { temp: temp_data6, time: time_data };
                successinitialized(myChart1, record_data1);
                successinitialized(myChart2, record_data2);
                successinitialized(myChart3, record_data3);
                successinitialized(myChart4, record_data4);
                successinitialized(myChart5, record_data5);
                successinitialized(myChart6, record_data6);

                //update chart with data
                console.log("Chart Data Initialize success" + response)
            }
        });
    };


    function update_chart_soak_all(myChart1, myChart2, myChart3, myChart4, myChart5, myChart6, myChart7, myChart8) {
        $.ajax({
            url: "_update_data_soak_all",
            type: "GET",
            success: function (response) {
                var temp_data1 = response.data.T_soak1;
                var temp_data2 = response.data.T_soak2;
                var temp_data3 = response.data.T_soak3;
                var temp_data4 = response.data.T_soak4;
                var temp_data5 = response.data.T_soak5;
                var temp_data6 = response.data.T_soak6;
                var temp_data7 = response.data.T_soak7;
                var temp_data8 = response.data.T_soak8;
                var time_data1 = response.data.chart_time1;
                var time_data2 = response.data.chart_time2;
                var time_data3 = response.data.chart_time3;
                var time_data4 = response.data.chart_time4;
                var time_data5 = response.data.chart_time5;
                var time_data6 = response.data.chart_time6;
                var time_data7 = response.data.chart_time7;
                var time_data8 = response.data.chart_time8;

                var new_data1 = [temp_data1, time_data1];
                var new_data2 = [temp_data2, time_data2];
                var new_data3 = [temp_data3, time_data3];
                var new_data4 = [temp_data4, time_data4];
                var new_data5 = [temp_data5, time_data5];
                var new_data6 = [temp_data6, time_data6];
                var new_data7 = [temp_data7, time_data7];
                var new_data8 = [temp_data8, time_data8];

                if (myChart1.data.labels.length >= 100) {
                    myChart1.data.labels.shift();
                    myChart1.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })
                }
                myChart2.data.labels.push(time_data2);
                myChart2.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data1[index]);
                })
                myChart1.update();

                if (myChart2.data.labels.length >= 100) {
                    myChart2.data.labels.shift();
                    myChart2.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })
                }
                myChart2.data.labels.push(time_data2);
                myChart2.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data2[index]);
                })
                myChart2.update();

                if (myChart3.data.labels.length >= 100) {
                    myChart3.data.labels.shift();
                    myChart3.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })
                }
                myChart3.data.labels.push(time_data3);
                myChart3.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data3[index]);
                })
                myChart3.update();

                if (myChart4.data.labels.length >= 100) {
                    myChart4.data.labels.shift();
                    myChart4.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })
                }
                myChart4.data.labels.push(time_data4);
                myChart4.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data4[index]);
                })
                myChart4.update();

                if (myChart5.data.labels.length >= 100) {
                    myChart5.data.labels.shift();
                    myChart5.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })
                }
                myChart5.data.labels.push(time_data5);
                myChart5.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data5[index]);
                })
                myChart5.update();

                if (myChart6.data.labels.length >= 100) {
                    myChart6.data.labels.shift();
                    myChart6.data.datasets.forEach((dataset) => {
                        dataset.data.shift();
                    })
                }
                myChart6.data.labels.push(time_data6);
                myChart6.data.datasets.forEach((dataset, index) => {
                    dataset.data.push(new_data6[index]);
                })
                myChart6.update();
            }
        })
   };

//update chart with data received.
function update_chart_soak1(myChart) {
    $.ajax({
        url: "_update_data_soak1",
        type: "GET",
        success: function (response) {
            var temp_data = response.data.T_soak1;
            //var valve_data = response.data.Valve_shed3_hot;
            var time_data = response.data.chart_time;
            var new_data = [temp_data, time_data];

            console.log("Received new Chart Data: " + new_data + " with time stamp: " + time_data);
            console.log(response.data)
            if (myChart.data.labels.length >= 100) {
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
//Chart2
function update_chart_soak2(myChart) {
    $.ajax({
        url: "_update_data_soak2",
        type: "GET",
        success: function (response) {
            var temp_data = response.data.T_soak2;
            //var valve_data = response.data.Valve_shed3_hot;
            var time_data = response.data.chart_time;
            var new_data = [temp_data, time_data];

            console.log("Received new Chart Data: " + new_data + " with time stamp: " + time_data);
            console.log(response.data)
            if (myChart.data.labels.length >= 50) {
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
//Chart3
function update_chart_soak3(myChart) {
    $.ajax({
        url: "_update_data_soak3",
        type: "GET",
        success: function (response) {
            var temp_data = response.data.T_soak3;
            //var valve_data = response.data.Valve_shed3_hot;
            var time_data = response.data.chart_time;
            var new_data = [temp_data, time_data];

            console.log("Received new Chart Data: " + new_data + " with time stamp: " + time_data);
            console.log(response.data)
            if (myChart.data.labels.length >= 50) {
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
//Chart4
function update_chart_soak4(myChart) {
    $.ajax({
        url: "_update_data_soak4",
        type: "GET",
        success: function (response) {
            var temp_data = response.data.T_soak4;
            //var valve_data = response.data.Valve_shed3_hot;
            var time_data = response.data.chart_time;
            var new_data = [temp_data, time_data];

            console.log("Received new Chart Data: " + new_data + " with time stamp: " + time_data);
            console.log(response.data)
            if (myChart.data.labels.length >= 50) {
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
//Chart4
function update_chart_soak5(myChart) {
    $.ajax({
        url: "_update_data_soak5",
        type: "GET",
        success: function (response) {
            var temp_data = response.data.T_soak5;
            //var valve_data = response.data.Valve_shed3_hot;
            var time_data = response.data.chart_time;
            var new_data = [temp_data, time_data];

            console.log("Received new Chart Data: " + new_data + " with time stamp: " + time_data);
            console.log(response.data)
            if (myChart.data.labels.length >= 50) {
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
//Chart4
function update_chart_soak6(myChart) {
    $.ajax({
        url: "_update_data_soak6",
        type: "GET",
        success: function (response) {
            var temp_data = response.data.T_soak6;
            //var valve_data = response.data.Valve_shed3_hot;
            var time_data = response.data.chart_time;
            var new_data = [temp_data, time_data];

            console.log("Received new Chart Data: " + new_data + " with time stamp: " + time_data);
            console.log(response.data)
            if (myChart.data.labels.length >= 50) {
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
//initiate the data retrieval process

initializedata_soak(myChart_soak1, myChart_soak2, myChart_soak3, myChart_soak4, myChart_soak5, myChart_soak6);
//setInterval(update_chart_soak_all, 1000, myChart_soak1, myChart_soak2, myChart_soak3, myChart_soak4, myChart_soak5, myChart_soak6)
setInterval(update_chart_soak1, 300000, myChart_soak1)
setInterval(update_chart_soak2, 300000, myChart_soak2)  //300000 is updated every 5 minutes
setInterval(update_chart_soak3, 300000, myChart_soak3)
setInterval(update_chart_soak4, 300000, myChart_soak4)
setInterval(update_chart_soak5, 300000, myChart_soak5)
setInterval(update_chart_soak6, 300000, myChart_soak6)
})

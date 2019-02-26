	$(document).ready(function() {

		$('#calendar').fullCalendar({


			dayRender: function (date, cell) {
			    $.ajax({
			        url: '/get_date_ajax',
			        type: "POST",
			        contentType: 'application/json;charset=UTF-8',		         
					dataType: "json",
			        success: function(response) {
		                 response.forEach(function(data){
			        		if(data.avaliable_day.split("T")[0] == date.format()){
			        			cell.css("background-color", "rgb(21, 178, 153)");			
			        		}
						});
			        }
			    })
			    $.ajax({
			        url: '/get_date_vacation_ajax',
			        type: "POST",
			        contentType: 'application/json;charset=UTF-8',		         
					dataType: "json",
			        success: function(response) {
			        	response.forEach(function(data){
			        		if(data.avaliable_day.split("T")[0] == date.format()){
			        			if(data.status == "Pending"){
			        				cell.css("background-color", "yellow");
			        			}
			        			if(data.status == "Accepted"){
			        				cell.css("background-color", "green");
			        			}
			        			if(data.status == "Declined"){
			        				cell.css("background-color", "red");
			        			}
			        		}
						});
			        }
			    })
			},
	

			dayRightclick: function(date, jsEvent, view) {

						var now = new Date();
						today = now.getFullYear() + '-'
                                + ('0' + (now.getMonth() +1) ).slice(-2)
                                + "-" +('0' + now.getDate()).slice(-2);

					    if (date.format() < today){
					    	alert('The previous days are disabled')
					    }
					    else
					    {
							operation = ''

	                        var moment = date.toDate();
	                        MyDateString = moment.getFullYear() + '-'
	                                + ('0' + (moment.getMonth() +1) ).slice(-2)
	                                + "-" +('0' + moment.getDate()).slice(-2);

	                        var thisdate = $('[data-date='+MyDateString+']')
	                        console.log(thisdate.css('background-color'))
	                        if (thisdate.css('backgroundColor') == "rgba(0, 0, 0, 0)"){
	                        	alert("This is not a valid vacation day")
	                        }
	                        else if (thisdate.css('backgroundColor') == "rgb(21, 178, 153)"){
	                        	thisdate.css({"backgroundColor": "yellow"});
	                        	operation = 'insert'
	                        }
	                        //yellow
	                        else if (thisdate.css('backgroundColor') == "rgb(255, 255, 0)"){
	                        	thisdate.css({"backgroundColor": "rgb(21, 178, 153)"});
	                        	operation = 'delete'
	                        }
	                        //red
	                        else if (thisdate.css('backgroundColor') == "rgb(255, 0, 0)"){
	                        	thisdate.css({"backgroundColor": "rgb(21, 178, 153)"});
	                        	operation = 'delete'
	                        }
	                        //green
	                        else if (thisdate.css('backgroundColor') == "rgb(0, 128, 0)"){
	                        	thisdate.css({"backgroundColor": "rgb(21, 178, 153)"});
	                        	operation = 'delete'
	                        }

	                        var data = {
								'date' : date.format(),
								'operation' : operation
							} 
							if (operation != ''){
								$.ajax({
							          type: "POST",
							          url: '/set_date_vacation_ajax',
							          data: JSON.stringify(data),
							          contentType: 'application/json;charset=UTF-8',		         
									  dataType: "json"
							   });
							}
						}
                        return false
		    },

			dayClick: function(date, jsEvent, view) {

				var now = new Date();
						today = now.getFullYear() + '-'
                                + ('0' + (now.getMonth() +1) ).slice(-2)
                                + "-" +('0' + now.getDate()).slice(-2);

				if (date.format() < today){
			    	alert('The previous days are disabled')
			    }
			    else
			    {
			
					var operation = ''

					if ($(this).css('backgroundColor') == "rgba(0, 0, 0, 0)"){
						$(this).css('background-color', "rgb(21, 178, 153)");
						operation = 'insert'

					}
					else if ($(this).css('backgroundColor') == "rgb(21, 178, 153)"){
						$(this).css('background-color', "rgba(0, 0, 0, 0)");
						operation = 'delete'
					}

					var data = {
						'date' : date.format(),
						'operation' : operation
					} 
					$.ajax({
				          type: "POST",
				          url: '/set_date_ajax',
				          data: JSON.stringify(data),
				          contentType: 'application/json;charset=UTF-8',		         
						  dataType: "json"
				   });
				}
			},	

			header: {
				left: 'prev,next',
				center: 'title',
				right: 'month'
			},
			aspectRatio: 2,
			defaultDate: new Date(),
			editable: true,
			eventLimit: true, 
		
		});

	});

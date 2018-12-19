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


                        if (thisdate.css('backgroundColor') == "rgba(0, 0, 0, 0)"){
                        	alert("This is not a valid vacation day")
                        }

                        else if (thisdate.css('backgroundColor') == "rgb(21, 178, 153)"){
                        	thisdate.css({"backgroundColor": "yellow"});
                        	operation = 'insert'
                        }

                        else if (thisdate.css('backgroundColor') == "rgb(255, 255, 0)"){
                        	thisdate.css({"backgroundColor": "rgb(21, 178, 153)"});
                        	operation = 'delete'
                        }

                        var data = {
							'date' : date.format(),
							'operation' : operation
						} 
						new_data = JSON.stringify(data)
						if (operation != ''){
							$.ajax({
						          type: "POST",
						          url: '/set_date_vacation_ajax',
						          data: new_data,
						          contentType: 'application/json;charset=UTF-8',		         
								  dataType: "json"
						   });
						}
					}
                  return false
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

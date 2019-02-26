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
			},
			aspectRatio: 2,
			defaultView: 'month',
			header: {
				left: 'prev,next',
				center: 'title',
				right: 'month'
			},
			defaultDate: new Date(),
			editable: true,
			eventLimit: true,
		});

	});

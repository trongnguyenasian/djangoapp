$(document).ready(function() {
            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function(e) {
                      if(input.name == "test")
                        $('#img-test').attr('src', e.target.result);
                      else
                        $('#img-training').attr('src', e.target.result);
                    }

                    reader.readAsDataURL(input.files[0]);
                }
            }

            $("#id_test").change(function() {
                readURL(this);
            });
            $("#id_training").change(function() {
                readURL(this);
            });
        })

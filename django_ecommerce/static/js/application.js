$(function () {

    $("#user_form").submit(function () {
        if ($("#credit-card").is(":visible")) {
            var form = this;
            var card = {
                number: $("#credit_card_number").val(),
                expMonth: $("#expiry_month").val(),
                expYear: $("#expiry_year").val(),
                cvc: $("#cvv").val()
            };

            Stripe.createToken(card, function (status, response) {
                if (status === 200) {
                    console.log(status, response);
                    $("#credit-card-errors").hide();
                    $("#last_4_digitss").val(response.card.last4);
                    $("#stripe_token").val(response.id);
                }
                // always submit form even with errors
                form.submit();
                });
        //else {
        //            $("#stripe-error-message").text(response.error.message);
        //            $("#credit-card-errors").show();
        //            $("#user_submit").attr("disabled", false);
        //        }
        //    });

            return false;

        }

        return true

    });

    $("#change-card a").click(function () {
        $("#change-card").hide();
        $("#credit-card").show();
        $("#credit_card_number").focus();
        return false;
    });

    //show status in the achievements
    $("show-achieve").click(function() {
        a = $("#achievements");
        l = $("#show-achieve");
        if (a.hasClass('hide')) {
            a.hide().removeClass('hide').slideDown('slow');
            l.html("Hide Achievements");
        } else {
            a.addClass('hide');
            l.html("Show Achievements");
        }
        return false;
    })

});

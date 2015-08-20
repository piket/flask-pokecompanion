$(function() {
    console.log('Poke Script loaded');

    $('.select-pokemon').submit(function(e) {
        e.preventDefault();

        var form = $(this);
        console.log($(location).attr('href') + form.attr('action'))
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize() + "&formId=" + form.attr('id')
        }).done(function(result) {
            console.log(result);
            var pokemon = JSON.parse(result);
            renderPokeStats(pokemon);
        }).error(function(err) {
            console.log("ERROR:",err);
        })
    });

    var addOptions = function(select, options) {
        select.children().remove();
        var optionStr = '<option selected></option>'
        for(var i = 0; i < options.length; i++) {
            optionStr += '<option value="' + options[i] + '">' + options[i] + '</option>';
        }
        select.append(optionStr);
    }

    var renderPokeStats = function(pokemon) {
        var display = '#pokemon-' + pokemon.form;
        debugger;
        // display.show();
        for(var key in pokemon.stats) {
            switch(key) {
                case 'abilities':
                case 'moves':
                    addOptions($(display + ' .'+key), pokemon.stats[key]);
                    break;
                case 'types':
                    var types = $(display + ' .type');
                    types.eq(0).val(pokemon.stats.types[0]);
                    types.eq(1).val(pokemon.stats.types[1]);
                    break;
                default:
                    $(display + ' .'+key).val(pokemon.stats[key]);
            }
        }
    }
});
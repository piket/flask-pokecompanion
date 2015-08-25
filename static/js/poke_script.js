$(function() {
    console.log('Poke Script loaded');

    // console.log(pokeArr);
    var enterFlag = false;

    $('.dropdown').hide();

    $('.dropdown').on('mousedown','li',function() {
        var item = $(this);
        var dropdown = item.parent();
        var input = dropdown.prev();
        input.val(item.text());
        dropdown.hide();
        dropdown.html('');
        // debugger;
    });

    $('.dropdown').on('mouseenter','li',function() {
        // hover over
        $('.hover-name').removeClass('hover-name');
        $(this).addClass('hover-name');
    }).on('mouseleave', 'li', function() {
        $(this).removeClass('hover-name');
    });

    $('.pokemon-name').on('keyup', function(e) {
        console.log(e.which)
        var text = $(this).val().toLowerCase();
        var dropdown = $(this).next('.dropdown');
        if(e.which !== 37 && e.which !== 38 && e.which !== 39 && e.which !== 40 && e.which !== 13) {
            // debugger;
            dropdown.html('');

            console.log(text)
            if(text === '') {
                dropdown.hide();
            } else {
                var list = pokeArr.filter(function(pokename) {
                    if(pokename.search(new RegExp('^' + text)) !== -1) {
                        dropdown.append('<li class="pokename-dropdown">'+pokename[0].toUpperCase() + pokename.substr(1) + '</li>');
                        return pokename;
                    }
                });
                console.log(list);
                if(list.length) {
                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            }
        } else if (e.which === 38) {
            // hit arrow up
            // enterFlag = true;
            var highlighted = $('.hover-name');
            var prev = highlighted.prev();

            if(highlighted.length > 0 && prev.length > 0) {
                highlighted.removeClass('hover-name');
            } else if (highlighted.length === 0) {
                prev = $('.pokename-dropdown').last();
            }
            prev.addClass('hover-name');
            $(this).val(prev.text());
        } else if (e.which === 40) {
            // hit arrow down
            // enterFlag = true;
            var highlighted = $('.hover-name');
            var next = highlighted.next();

            if(highlighted.length > 0 && next.length > 0) {
                highlighted.removeClass('hover-name');
            } else if (highlighted.length === 0) {
                next = $('.pokename-dropdown').first();
            }
            next.addClass('hover-name');
            $(this).val(next.text());
        } //else if (e.which === 13) {
        //     // hit enter
        //     var highlighted = $('.hover-name');
        //     if(highlighted.length > 0) {
        //         $(this).val(highlighted.text());
        //         dropdown.hide();
        //         dropdown.html('');
        //     }
        // }
    });

    $('.pokemon-name').blur(function(e) {
        // console.log(e)
        $(this).next('.dropdown').html('').hide();
    });

    var evDisplays = $('.ev-display').hide();
    var ivDisplays = $('.iv-display').hide();

    var showOtherStats = function() {
        // evDisplays.slideUp();
        // ivDisplays.slideUp();
        var btn = $(this);
        var display = $('#' + btn.attr('data-display'));
        var id = btn.attr('data-pokemon-id');


        if(!display.hasClass('active-'+id)) {
            $('.active-'+id).slideUp().removeClass('active-'+id);
            display.slideDown();
            display.addClass('active-'+id);
        } else {
            $('.active-'+id).slideUp().removeClass('active-'+id);
        }
    }

    $('.show-evs').click(showOtherStats);
    $('.show-ivs').click(showOtherStats);

    var changeAllVals = function() {
        var ref = $(this).attr('data-ref');
        var val = $(this).attr('data-val');
        $('#pokemon-'+ref).val(val);
        calculateStats(parseInt(ref));
    }

    $('.max-btn').click(changeAllVals);
    $('.reset-btn').click(changeAllVals);

    $('.select-pokemon').submit(function(e) {
        e.preventDefault();
        console.log("Enter Flag:",enterFlag);
        if(enterFlag) {
            enterFlag = false;
        } else {
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
        }
    });

    var calculateStats = function(pokeId) {
        var level = $('#pokemon-'+pokeId+'-level');
        var levelStats = $('#pokemon-'+pokeId+'-level-stats').find('.level-stat');
        var baseStats = $('#pokemon-'+pokeId+'-base-stats');
        var ivs = $('#pokemon-'+pokeId+'-ivs');
        var evs = $('#pokemon-'+pokeId+'-evs');
        var nature = $('#pokemon-'+pokeId+'-nature');

        if(nature.val()) {
            nature = nature.find('[value='+nature.val()+']')
            var natureMod = {
                bonus: nature.attr('data-bonus'),
                penalty: nature.attr('data-penalty')
            }
        } else {
            var natureMod = {bonus: 'None', penalty: 'None'};
        }

        for(var i = 0; i < levelStats.length; i++) {
            var stat = levelStats.eq(i).attr('data-name');
            var base = parseFloat(baseStats.find('.'+stat).val());
            var iv = parseInt(ivs.find('.'+stat).val());
            var ev = parseInt(evs.find('.'+stat).val());

            genStat(base, iv, ev, natureMod, parseFloat(level.val()), levelStats.eq(i));
        }
    }

    $('.ev-stat').on('change', function() {
        var entry = $(this);
        var val = entry.val();

        if(val > 255) {
            entry.val(255);
        } else if(val < 0) {
            entry.val(0)
        } else {
            calculateStats(entry.attr('data-id'));
        }
    });

    $('.iv-stat').on('change', function() {
        var entry = $(this);
        var val = entry.val();

        if(val > 32) {
            entry.val(32);
        } else if(val < 0) {
            entry.val(0)
        } else {
            calculateStats(entry.attr('data-id'));
        }
    });

    $('.level').change(function() {
        calculateStats($(this).attr('data-id'));
    });

    $('.nature').change(function() {
        calculateStats($(this).attr('data-id'));
    });

    var addOptions = function(select, options, text) {
        select.children().remove();
        var optionStr = '<option selected class="default-selection" value="">'+text+'</option>'
        for(var i = 0; i < options.length; i++) {
            optionStr += '<option value="' + options[i] + '">' + options[i] + '</option>';
        }
        select.append(optionStr);
    }

    var renderPokeStats = function(pokemon) {
        var display = '#pokemon-' + pokemon.form;
        $('#pokemon-exist-'+pokemon.form).val(pokemon.id);
        // debugger;
        // display.show();
        var text = '';
        for(var key in pokemon.stats) {
            switch(key) {
                case 'abilities':
                    text = 'No ability';
                    addOptions($(display + ' .'+key), pokemon.stats[key], text);
                    break;
                case 'moves':
                    text = 'No move';
                    addOptions($(display + ' .'+key), pokemon.stats[key], text);
                    break;
                case 'types':
                    var types = $(display + ' .type');
                    type1 = pokemon.stats.types[0][0].toUpperCase() + pokemon.stats.types[0].substr(1);
                    type2 = pokemon.stats.types[1] ? pokemon.stats.types[1][0].toUpperCase() + pokemon.stats.types[1].substr(1) : '';
                    types.eq(0).val(type1);
                    types.eq(1).val(type2);
                    break;
                default:
                    $(display + ' .base-stat.'+key).val(pokemon.stats[key]);
            }
        }
        calculateStats(pokemon.form);
    }

    function genStat(base, iv, ev, nature, level, input) {
        var evCalc = ev ? ev/4.0 : 0;
        var mod = {addBase: 0, addAll: 5, nature: 1}

        switch(input.attr('name')) {
            case 'hp-level':
                mod.addBase = 100;
                mod.addAll = 10;
                break;
            case 'attack-level':
                if(nature.bonus === 'attack') {
                    mod.nature = 1.1;
                } else if(nature.penalty === 'attack') {
                    mod.nature = 0.9;
                }
                break;
            case 'defense-level':
                if(nature.bonus === 'defense') {
                    mod.nature = 1.1;
                } else if(nature.penalty === 'defense') {
                    mod.nature = 0.9;
                }
                break;
            case 'sp_attack-level':
                if(nature.bonus === 'sp_attack') {
                    mod.nature = 1.1;
                } else if(nature.penalty === 'sp_attack') {
                    mod.nature = 0.9;
                }
                break;
            case 'sp_defense-level':
                if(nature.bonus === 'sp_defense') {
                    mod.nature = 1.1;
                } else if(nature.penalty === 'sp_defense') {
                    mod.nature = 0.9;
                }
                break;
            case 'speed-level':
                if(nature.bonus === 'speed') {
                    mod.nature = 1.1;
                } else if(nature.penalty === 'speed') {
                    mod.nature = 0.9;
                }
                break;
        }
        input.val(Math.floor((((((2*base) + iv + evCalc + mod.addBase)*level)/100) + mod.addAll)*mod.nature));
    }

    $('.moves').on('change', function() {
        var move = $(this);
        if(move.val()) {
            move.next('.trigger').show();
        } else {
            move.next('.trigger').hide();
        }
    });

    $('.trigger').click(function() {
        var trigger = $(this);
        var move = $(this).prev('.moves');
        var originId = trigger.attr('data-id');
        var targetId = trigger.val();

        $.ajax({
            url: '/api/attack',
            method: 'PUT',
            data: {
                move: move.val(),
                origin: {
                    name: $('#'+originId+' .pokemon-name').val(),
                    id: $('#pokemon-exist-'+originId).val(),
                    level: $('#pokemon-'+originId+'-level').val(),
                    hp: $('#pokemon-'+originId+'-level-stats .hp').val(),
                    attack: $('#pokemon-'+originId+'-level-stats .attack').val(),
                    defense: $('#pokemon-'+originId+'-level-stats .defense').val(),
                    sp_attack: $('#pokemon-'+originId+'-level-stats .sp_attack').val(),
                    sp_defense: $('#pokemon-'+originId+'-level-stats .sp_defense').val(),
                    speed: $('#pokemon-'+originId+'-level-stats .speed').val()
                },
                target: {
                    name: $('#'+targetId+' .pokemon-name').val(),
                    id: $('#pokemon-exist-'+targetId).val(),
                    hp: $('#pokemon-'+targetId+'-level-stats .hp').val(),
                    attack: $('#pokemon-'+targetId+'-level-stats .attack').val(),
                    defense: $('#pokemon-'+targetId+'-level-stats .defense').val(),
                    sp_attack: $('#pokemon-'+targetId+'-level-stats .sp_attack').val(),
                    sp_defense: $('#pokemon-'+targetId+'-level-stats .sp_defense').val(),
                    speed: $('#pokemon-'+targetId+'-level-stats .speed').val()
                }
            }
        }).done(function(result) {
            alert(result.origin + ' used '+result.move+' against enemy '+result.target+' and '+result.result);
            console.log("ATTACK RESULT:",result);
        }).error(function(err) {
            console.log("ERROR:",err);
        });
    });
});
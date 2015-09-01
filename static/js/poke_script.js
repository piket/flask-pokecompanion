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
        // input.sumbit();
        dropdown.parent().parent().trigger('submit');
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
    var stageDisplays = $('.stage-display').hide();

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
    $('.show-stages').click(showOtherStats);

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
            form.find('.dropdown').hide().html('');
            console.log($(location).attr('href') + form.attr('action'))
            $.ajax({
                url: form.attr('action'),
                method: 'POST',
                // dataType: 'json',
                data: form.serialize() + "&formId=" + form.attr('id')
            }).done(function(result) {
                console.log(result);
                var pokemon = JSON.parse(result);
                renderPokeStats(pokemon);
                $('#pokemon-exist-'+pokemon.form).val(pokemon.id);
                $.each($('.target').children(), function(i, option) {
                    val = $(option).val().split('.');
                    if(val[0] === pokemon.form) {
                        $(option).remove();
                    }
                });
                $('.target').append('<option value="'+pokemon.form+'.'+pokemon.id+'">'+pokemon.name[0].toUpperCase() + pokemon.name.substr(1)+'</option>');
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
        var stages = $('#pokemon-'+pokeId+'-stages');
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
            var stage = stat !== 'hp' ? parseInt(stages.find('.'+stat).val()) : 0;

            genStat(base, iv, ev, stage, natureMod, parseFloat(level.val()), levelStats.eq(i));
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

    $('.stage-stat').on('change', function() {
        var entry = $(this);
        var val = entry.val();

        if(val > 6) {
            entry.val(6);
        } else if (val < -6) {
            entry.val(-6);
        } else if(!entry.hasClass('critical')) {
            calculateStats(entry.attr('data-id'));
        }

        if(entry.hasClass('critical') && val > 3) {
            entry.val(3);
        } else if(entry.hasClass('critical') && val < 0) {
            entry.val(0);
        }
    })

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
                    addOptions($(display + ' .'+key), pokemon[key], text);
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

    function genStat(base, iv, ev, stage, nature, level, input) {
        var evCalc = ev ? ev/4.0 : 0;
        var stages = {'-6':2/8.0, '-5':2/7.0, '-4':2/6.0, '-3':2/5.0, '-2':2/4.0, '-1':2/3.0, '0':1, '1':3/2.0, '2':4/2.0, '3':5/2.0, '4':6/2.0, '5':7/2.0, '6':8/2.0}
        var mod = {addBase: 0, addAll: 5, nature: 1, stage: stages[stage]}

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
        input.val(Math.floor((((((2 * base) + iv + evCalc + mod.addBase) * level)/100) + mod.addAll) * mod.nature * mod.stage));
    }

    $('.trigger-display').hide();

    $('.moves').on('change', function() {
        var move = $(this);
        if(move.val()) {
            move.parent().next('.trigger-display').show();
        } else {
            move.parent().next('.trigger-display').hide();
        }
    });

    $('.trigger').click(function() {
        var trigger = $(this).attr('data-move');
        var move = $('#pokemon-'+trigger);
        var originId = trigger.substring(0,trigger.indexOf('-'));
        var targetId = $('#target-'+trigger).val().split('.');
        var targetDbId = targetId[1];
        targetId = targetId[0]

        console.log("originId:",originId,'targetDbId:',targetDbId, 'targetId:', targetId);

        var data = {
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

        switch($('#pokemon-'+originId+'-stages .critical').val()) {
            case '0':
                data.origin.crit_chance = 16;
                break;
            case '1':
                data.origin.crit_chance = 8;
                break;
            case '2':
                data.origin.crit_chance = 2;
                break;
            case '3':
                data.origin.crit_chance = 1;
                break;
            default:
                data.origin.crit_chance = 16;
                break;
        }
        switch($('#pokemon-'+originId+'-stages .accuracy').val()) {
            case '-6':
                data.origin.accuracy = 3/9.0;
                break;
            case '-5':
                data.origin.accuracy = 3/8.0;
                break;
            case '-4':
                data.origin.accuracy = 3/7.0;
                break;
            case '-3':
                data.origin.accuracy = 3/6.0;
                break;
            case '-2':
                data.origin.accuracy = 3/5.0;
                break;
            case '-1':
                data.origin.accuracy = 3/4.0;
                break;
            case '0':
                data.origin.accuracy = 3/3.0;
                break;
            case '1':
                data.origin.accuracy = 4/3.0;
                break;
            case '2':
                data.origin.accuracy = 5/3.0;
                break;
            case '3':
                data.origin.accuracy = 6/3.0;
                break;
            case '4':
                data.origin.accuracy = 7/3.0;
                break;
            case '5':
                data.origin.accuracy = 8/3.0;
                break;
            case '6':
                data.origin.accuracy = 9/3.0;
                break;
            default:
                data.origin.accuracy = 1;
                break;
        }
        switch($('#pokemon-'+targetId+'-stages .evasion').val()) {
            case '-6':
                data.target.evasion = 3/9.0;
                break;
            case '-5':
                data.target.evasion = 3/8.0;
                break;
            case '-4':
                data.target.evasion = 3/7.0;
                break;
            case '-3':
                data.target.evasion = 3/6.0;
                break;
            case '-2':
                data.target.evasion = 3/5.0;
                break;
            case '-1':
                data.target.evasion = 3/4.0;
                break;
            case '0':
                data.target.evasion = 3/3.0;
                break;
            case '1':
                data.target.evasion = 4/3.0;
                break;
            case '2':
                data.target.evasion = 5/3.0;
                break;
            case '3':
                data.target.evasion = 6/3.0;
                break;
            case '4':
                data.target.evasion = 7/3.0;
                break;
            case '5':
                data.target.evasion = 8/3.0;
                break;
            case '6':
                data.target.evasion = 9/3.0;
                break;
            default:
                data.target.evasion = 1;
                break;
        }
        console.log('DATA:',data)

        $.ajax({
            url: '/api/attack',
            method: 'POST',
            // contentType: 'application/json',
            data: data,
            dataType: 'json'
        }).done(function(result) {
            if(result.response) {
                if(result.crit) {
                    style = 'yellow black-text';
                } else if(result.result.indexOf('missed') !== -1) {
                    style = 'red';
                } else {
                    style = 'green';
                }

                Materialize.toast(result.origin + ' used '+result.move+' against enemy '+result.target+' and '+result.result, 3000, style);
            }
            console.log("ATTACK RESULT:",result);
        }).error(function(err) {
            console.log("ERROR:",err);
        });
    });
});
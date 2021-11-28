(function($) {
    'use strict';

    var apiUrl = 'https://coincap.io';
    var socket = io.connect('https://socket.coincap.io');

    var dataTableWidget = null;
    var $tableWidget = $('#RealTimeCryptoPricing');
    var $pluginWrapper = $('#crypto-live--wrapper');


    // real-time update coins info
    socket.on('trades', function(response) {
        var $row = $tableWidget.find('tr[data-coin="'+ response.coin +'"]');

        if ($row.length) {
            var cssClass = (response.msg.price > $row.attr('data-price')) ? 'price-plus' : 'price-minus';

            $row.addClass(cssClass);
            $row.attr('data-price', response.msg.price);
            $row.find('.market-cap').html('$<span>'+ response.msg.mktcap +'</span>');
            $row.find('.price').html('$<span>'+ response.msg.price +'</span>');
            $row.find('.vwap24').html('$<span>'+ response.msg.vwapData +'</span>');
            $row.find('.supply').text(response.msg.supply);
            $row.find('.volume24').html('$<span>'+ response.msg.volume +'</span>');
            $row.find('.change24').text(response.msg.cap24hrChange +'%');

            initColumnNumbers();
            setTimeout(function() {
                $row.removeClass('price-plus price-minus');
            }, 300);
        }
    });

    $(document).ready(function() {
        getWidgetTableData();
    });

    // format numbers
    var initColumnNumbers = function() {
        $tableWidget.find('.volume24 span, .market-cap span').number(true, 2, '.', ',');
        $tableWidget.find('.price span, .vwap24 span').number(true, 4, '.', ',');
        $tableWidget.find('.supply').number(true);
    };

    // main widget: init dataTable
    var initWidgetTable = function() {
        dataTableWidget = $tableWidget.DataTable({
            info: $tableWidget.data('info'),
            paging: $tableWidget.data('paging'),
            scrollX: $tableWidget.data('scrollx'),
            ordering: $tableWidget.data('ordering'),
            searching: $tableWidget.data('searching')
        });
        initColumnNumbers();
    };

    // main widget: get all coins data
    var getWidgetTableData = function() {
        $.ajax({
            url: apiUrl + '/front',
            method: 'GET',
            beforeSend: function() {
                $pluginWrapper.find('.load-container').removeClass('hidden');
            },
            success: function(coins) {
                if (coins.length) {
                    var tableRows = '';

                    for (var i = 0; i < coins.length; i++) {
                        tableRows += '<tr class="open-chart" data-coin="'+ coins[i].short +'">';
                        tableRows += '<td class="number">'+ (i + 1) +'</td>';
                        tableRows += '<td class="name">'+ coins[i].long +' '+ coins[i].short +'</td>';
                        tableRows += '<td class="market-cap">$<span>'+ coins[i].mktcap +'</span></td>';
                        tableRows += '<td class="price">$<span>'+ coins[i].price +'</span></td>';
                        tableRows += '<td class="vwap24">$<span>'+ coins[i].vwapData +'</span></td>';
                        tableRows += '<td class="supply">'+ coins[i].supply +'</td>';
                        tableRows += '<td class="volume24">$<span>'+ coins[i].volume +'</span></td>';
                        tableRows += '<td class="change24">'+ coins[i].cap24hrChange +'%</td>';
                        tableRows += '</tr>';
                    }

                    $tableWidget.find('tbody').html(tableRows);
                    initWidgetTable();
                    createCoinChart();
                }
            },
            complete: function() {
                $tableWidget.removeClass('hidden');
                $pluginWrapper.find('.load-container').addClass('hidden');
            }
        });
    };

    // main widget: create coin chart
    var createCoinChart = function() {
        $('body').on('click', '#RealTimeCryptoPricing .open-chart', function(e) {
            e.preventDefault();

            var self = $(this);
            var coin = self.closest('tr').data('coin');
            var labels = []; var marketCapData = []; var volumeData = []; var priceData = [];

            if (self.closest('tr').next().hasClass('chart-row')) {
                $tableWidget.find('.chart-row').remove();
                return true;
            }

            $.ajax({
                url: apiUrl + '/history/365day/' + coin,
                method: 'GET',
                beforeSend: function() {
                    $tableWidget.find('.chart-row').remove();
                    $pluginWrapper.find('.load-container').removeClass('hidden');
                },
                success: function(history) {
                    $.each(history.price, function(i, value) {
                        priceData.push(value[1]);
                    });
                    $.each(history.market_cap, function(i, value) {
                        labels.push(value[0]);
                        marketCapData.push(value[1]);
                    });
                    $.each(history.volume, function(i, value) {
                        volumeData.push(value[1]);
                    });

                    var chartRow = '<tr class="chart-row"><td colspan="8"><canvas id="crypto-live--chart"></canvas></td></tr>';
                    $(chartRow).insertAfter(self.closest('tr'));

                    setTimeout(function() {
                        initCoinChart(labels, coin, priceData, volumeData, marketCapData);
                        $pluginWrapper.find('.load-container').addClass('hidden');
                    }, 500);
                }
            });
        })
    };

    // main widget: init coin chart
    var initCoinChart = function(labels, coin, priceData, volumeData, marketCapData) {
        var ctx = document.getElementById('crypto-live--chart').getContext('2d');
        var config = {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: coin + ' - Price',
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgb(75, 192, 192)',
                    data: priceData
                }, {
                    label: coin + ' - Volume',
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgb(54, 162, 235)',
                    data: volumeData
                }, {
                    label: coin + ' - Market Cap',
                    borderColor: 'rgb(255, 159, 64)',
                    backgroundColor: 'rgb(255, 159, 64)',
                    data: marketCapData
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: false
                },
                tooltips: {
                    mode: 'index',
                    position: 'nearest',
                    intersect: false,
                    callbacks: {
                        title: function(tooltipItems) {
                            return moment(tooltipItems[0].xLabel).format('dddd, MMM DD, HH:mm:ss');
                        },
                        label: function(tooltipItems, data) {
                            return data.datasets[tooltipItems.datasetIndex].label +': $'+ $.number(tooltipItems.yLabel, 2, '.', ',');
                        }
                    }
                },
                hover: {
                    mode: 'index'
                },
                elements: {
                    point: {
                        radius: 0
                    }
                },
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            displayFormats: {
                                quarter: 'MMM YYYY'
                            }
                        }
                    }],
                    yAxes: [{
                        stacked: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + $.number(value, 2, '.', ',');
                            }
                        }
                    }]
                }
            }
        };

        new Chart(ctx, config);
    };
})(jQuery);
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#!/usr/bin/perl
use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use Term::ANSIColor;

sub format_number {
    my ($number) = @_;
    return sprintf("%.8f", $number);
}

sub format_price {
    my ($price) = @_;
    return sprintf("%.8f", $price);
}

while (1) {
    system('clear');

    my $url = 'https://api.txbit.io/api/public/getorderbook?market=NEOX/USDT&type=both';
    my $ua = LWP::UserAgent->new;
    my $response = $ua->get($url);

    die "Error: " . $response->status_line unless $response->is_success;

    my $data = decode_json($response->decoded_content);
    my $buy_orders = $data->{result}{buy};
    my $sell_orders = $data->{result}{sell};

    print "Buy Orders:\n";
    print "+----------------+-------------------+-----------------------+----------------------+-------------+\n";
    print "| Order Number   | Unit Price (USDT) | Total Order Amount    | Total NEOX Amount    | Slippage    |\n";
    print "+----------------+-------------------+-----------------------+----------------------+-------------+\n";

    my $buy_order_count = scalar(@$buy_orders);
    my $buy_order_number = 1;
    for (my $i = 0; $i < $buy_order_count && $buy_order_number <= 25; $i++) {
        my $order = $buy_orders->[$i];
        my $unit_price = format_price($order->{Rate});
        my $total_order_amount = format_number($order->{Rate} * $order->{Quantity});
        my $total_neox_amount = format_number($order->{Quantity});
        my $slippage = ($i > 0 && $buy_orders->[$i - 1]->{Rate} != 0) ? (($order->{Rate} - $buy_orders->[$i - 1]->{Rate}) / $buy_orders->[$i - 1]->{Rate}) * 100 : 0;
        printf("| %15d | %17s | \$%21s | %20s | %11.2f%% |\n", $buy_order_number, $unit_price, $total_order_amount, $total_neox_amount, $slippage);
        $buy_order_number++;
    }

    print "+----------------+-------------------+-----------------------+----------------------+-------------+\n";

    print "Sell Orders:\n";
    print "+----------------+-------------------+-----------------------+----------------------+-------------+\n";
    print "| Order Number   | Unit Price (USDT) | Total Order Amount    | Total NEOX Amount    | Slippage    |\n";
    print "+----------------+-------------------+-----------------------+----------------------+-------------+\n";

    my $sell_order_count = scalar(@$sell_orders);
    for (my $i = $sell_order_count - 1; $i >= 0 && $i >= $sell_order_count - 25; $i--) {
        my $order = $sell_orders->[$i];
        my $order_number = $sell_order_count - $i;
        my $unit_price = format_price($order->{Rate});
        my $total_order_amount = format_number($order->{Quantity} * $order->{Rate});
        my $total_neox_amount = format_number($order->{Quantity});
        my $slippage = ($i < $sell_order_count - 1 && $sell_orders->[$i + 1]->{Rate} != 0) ? (($order->{Rate} - $sell_orders->[$i + 1]->{Rate}) / $sell_orders->[$i + 1]->{Rate}) * 100 : 0;
        printf("| %15d | %17s | \$%21s | %20s | %11.2f%% |\n", $order_number, $unit_price, $total_order_amount, $total_neox_amount, $slippage);
    }

    print "+----------------+-------------------+-----------------------+----------------------+-------------+\n";

    sleep(30);
}

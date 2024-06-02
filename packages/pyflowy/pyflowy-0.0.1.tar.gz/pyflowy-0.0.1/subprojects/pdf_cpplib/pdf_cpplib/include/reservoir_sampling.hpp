#pragma once
#include <cstddef>
#include <queue>
#include <random>
#include <utility>
#include <vector>

#pragma once

namespace ProbabilityDist::ReservoirSampling
{

/**
 * @brief Draw k non-repeating random numbers in the interval [0,n].
 * the probability to draw a number i, is given by the weight callback
 * as weight(i)
 */
template<typename WeightCallbackT, typename Generator>
std::vector<std::size_t> reservoir_sampling_A_ExpJ( size_t k, size_t n, WeightCallbackT weight, Generator & gen )
{
    if( k == 0 )
        return {};

    std::uniform_real_distribution<double> distribution( 0.0, 1.0 );

    std::vector<size_t> reservoir( k );
    using QueueItemT = std::pair<size_t, double>;

    auto compare = []( const QueueItemT & item1, const QueueItemT & item2 ) { return item1.second > item2.second; };
    std::priority_queue<QueueItemT, std::vector<QueueItemT>, decltype( compare )> H;

    size_t idx = 0;
    while( ( idx < n ) && ( H.size() < k ) )
    {
        const double r = std::pow( distribution( gen ), 1.0 / weight( idx ) );
        H.push( { idx, r } );
        idx++;
    }

    double X = std::log( distribution( gen ) ) / std::log( H.top().second );
    while( idx < n )
    {
        const auto w = weight( idx );
        X -= w;
        if( X <= 0 )
        {
            const auto t = std::pow( H.top().second, w );
            const auto uniform_from_t_to_one
                = distribution( gen ) * ( 1.0 - t ) + t; // Random number in interval [t, 1.0]
            const auto r = std::pow( uniform_from_t_to_one, 1.0 / w );
            H.pop();
            H.push( { idx, r } );
            X = std::log( distribution( gen ) ) / std::log( H.top().second );
        }
        idx++;
    }

    auto res = std::vector<std::size_t>( H.size() );

    for( size_t i = 0; i < k; i++ )
    {
        res[i] = H.top().first;
        H.pop();
    }

    return res;
}

} // namespace ProbabilityDist::ReservoirSampling

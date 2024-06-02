#pragma once
#include "erfinv.hpp"
#include <limits>
#include <optional>
#include <random>

namespace ProbabilityDist
{

/**
 * @brief Power law distribution for random numbers.
 * A continuous random distribution on the range [eps, infty)
 * with p(x) ~ x^(-gamma)
 * Including normalization the PDF is
 * p(x) = (1-gamma)/(1-eps^(1-gamma)) * x^(-gamma)
 */
template<typename ScalarT = double>
class power_law_distribution
{
private:
    ScalarT eps;
    ScalarT gamma;
    std::uniform_real_distribution<ScalarT> dist
        = std::uniform_real_distribution<ScalarT>( 0.0, 1.0 ); // Uniform random variable for activities

public:
    power_law_distribution( ScalarT eps, ScalarT gamma ) : eps( eps ), gamma( gamma ) {}

    template<typename Generator>
    ScalarT operator()( Generator & gen )
    {
        return inverse_cdf( dist( gen ) );
    }

    ScalarT pdf( ScalarT x )
    {
        return ( 1.0 - gamma ) / ( 1.0 - std::pow( eps, ( 1 - gamma ) ) * std::pow( x, ( -gamma ) ) );
    }

    ScalarT inverse_cdf( ScalarT x )
    {
        return std::pow(
            ( 1.0 - std::pow( eps, ( 1.0 - gamma ) ) ) * x + std::pow( eps, ( 1.0 - gamma ) ),
            ( 1.0 / ( 1.0 - gamma ) ) );
    }

    ScalarT mean()
    {
        return -( 1.0 - gamma ) / ( 2.0 - gamma ) * std::pow( eps, 2.0 - gamma )
               / ( 1.0 - std::pow( eps, 1.0 - gamma ) );
    }
};

/**
 * @brief Truncated normal distribution
 * A continuous random distribution on the range [eps1, eps2]
 * If eps1 has no value, it is assumed to be -infty
 * If eps2 has no value, it is assumed to be infty
 * with p(x) ~ e^(-(x-mean)^2/(2 sigma^2))
 */
template<typename ScalarT = double>
class truncated_normal_distribution
{
private:
    ScalarT mean{};
    ScalarT sigma{};
    std::optional<ScalarT> eps1{};
    std::optional<ScalarT> eps2{};
    std::uniform_real_distribution<ScalarT> uniform_dist{};
    double cdf_n_eps2;
    double cdf_n_eps1;

    ScalarT inverse_cdf_gauss( ScalarT y )
    {
        return Math::erfinv( 2.0 * y - 1 ) * std::sqrt( 2.0 ) * sigma + mean;
    }

    ScalarT cdf_gauss( ScalarT x )
    {
        return 0.5 * ( 1 + std::erf( ( x - mean ) / ( sigma * std::sqrt( 2.0 ) ) ) );
    }

    ScalarT pdf_gauss( ScalarT x )
    {
        return 1.0 / ( sigma * std::sqrt( 2 * Math::pi ) ) * std::exp( -0.5 * std::pow( ( ( x - mean ) / sigma ), 2 ) );
    }

public:
    truncated_normal_distribution(
        ScalarT mean, ScalarT sigma, std::optional<ScalarT> eps1, std::optional<ScalarT> eps2 )
            : mean( mean ), sigma( sigma ), eps1( eps1 ), eps2( eps2 ), uniform_dist( 0, 1 )
    {

        // If eps1 has no value, it is assumed to be -infty
        if( eps1.has_value() )
        {
            cdf_n_eps1 = cdf_gauss( eps1.value() );
        }
        else
        {
            eps1 = -std::numeric_limits<ScalarT>::infinity();
            cdf_n_eps1 = 0;
        }

        // If eps2 has no value, it is assumed to be infty
        if( eps2.has_value() )
        {
            cdf_n_eps2 = cdf_gauss( eps2.value() );
        }
        else
        {
            eps2 = std::numeric_limits<ScalarT>::infinity();
            cdf_n_eps2 = 1.0;
        }
    }

    template<typename Generator>
    ScalarT operator()( Generator & gen )
    {
        return inverse_cdf( uniform_dist( gen ) );
    }

    ScalarT inverse_cdf( ScalarT y )
    {
        return inverse_cdf_gauss( y * ( cdf_n_eps2 - cdf_n_eps1 ) + cdf_n_eps1 );
    }

    ScalarT pdf( ScalarT x )
    {
        if( x < eps1.value() || x > eps2.value() )
            return 0.0;
        else
            return 1.0 / ( cdf_n_eps2 - cdf_n_eps1 ) * pdf_gauss( x );
    }
};

/**
 * @brief Bivariate normal distribution
 * with mean mu = [0,0]
 * and covariance matrix Sigma = [[1, cov], [cov, 1]]
 * |cov| < 1 is required
 */
template<typename ScalarT = double>
class bivariate_normal_distribution
{
private:
    ScalarT covariance;
    std::normal_distribution<ScalarT> normal_dist{};

public:
    bivariate_normal_distribution( ScalarT covariance ) : covariance( covariance ) {}

    template<typename Generator>
    std::array<ScalarT, 2> operator()( Generator & gen )
    {
        ScalarT n1 = normal_dist( gen );
        ScalarT n2 = normal_dist( gen );

        ScalarT r1 = n1;
        ScalarT r2 = covariance * n1 + std::sqrt( 1.0 - covariance * covariance ) * n2;

        return { r1, r2 };
    }
};

template<typename ScalarT, typename dist1T, typename dist2T>
class bivariate_gaussian_copula
{
private:
    ScalarT covariance;
    bivariate_normal_distribution<ScalarT> biv_normal_dist{};

    // Cumulative probability function for gaussian with mean 0 and variance 1
    ScalarT cdf_gauss( ScalarT x )
    {
        return 0.5 * ( 1 + std::erf( ( x ) / std::sqrt( 2.0 ) ) );
    }

    dist1T dist1;
    dist2T dist2;

public:
    bivariate_gaussian_copula( ScalarT covariance, dist1T dist1, dist2T dist2 )
            : covariance( covariance ),
              biv_normal_dist( bivariate_normal_distribution( covariance ) ),
              dist1( dist1 ),
              dist2( dist2 )
    {
    }

    template<typename Generator>
    std::array<ScalarT, 2> operator()( Generator & gen )
    {
        // 1. Draw from bivariate gaussian
        auto z = biv_normal_dist( gen );
        // 2. Transform marginals to unit interval
        std::array<ScalarT, 2> z_unit = { cdf_gauss( z[0] ), cdf_gauss( z[1] ) };
        // 3. Apply inverse transform sampling
        std::array<ScalarT, 2> res = { dist1.inverse_cdf( z_unit[0] ), dist2.inverse_cdf( z_unit[1] ) };
        return res;
    }
};

} // namespace ProbabilityDist
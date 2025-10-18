## Buying vs renting your home

It’s a decision nearly everyone will make in their lives (at least once) - “Do I buy my home or rent it?” People sometimes say that “rent money is dead money.” but there’s a lot more to the story than that. Those who rent often argue that owning a property is just too expensive and they may choose to put their extra savings into other investments. Furthermore, not many people talk about the additional costs with owning a home.
<img src="{{url_for('static', filename='blog/house.svg')}}" class="center" style="display: block;margin-left:auto;margin-right:auto;width:350px;height:350px">
I don’t have a strong view either way. The answer depends on you and your stage in life - your lifestyle balanced with financial considerations. For the financial component, it’s important to make an informed decision based on all sources of unbiased information. What you need to do is [calculate]({{url_for('property_page')}}) in investment terms what renting vs buying looks like for your own circumstances.

### Lifestyle considerations
It’s important to start with lifestyle; think about what you want your life to look like and then figure how to fund it. For example if you’re fresh out of school or uni and you want to travel, you might think twice about putting your savings into a new home (similarly if at any time in your life you want to take a sabbatical or study). Make sure you have an idea how much you plan to spend each month, since mortgage repayments and house costs will limit what you can spend. Perhaps you want a place in which to lay your roots and settle down, and then finally you can do things like put hooks in the wall, or paint the bedrooms. All of these things are unique to you.

### Financial considerations
Fortunately financial considerations are easier since they’re measurable. You give up some money as a deposit on a home, then you re-pay monthly amounts (which includes interest) for 25 years and the home is yours! Hopefully in that time it will go up in value and you’ll make a profit when you sell. There’s more to it than that however as several aspects are often forgotten, including:

  1. How much money will you need for costs in buying your home  (stamp-duty/legal etc)?
  2. How much money will you need to run your home (maintenance/repairs/upgrades etc)?
  3. How much money will you need for costs in selling your home (commissions etc)?
  4. Will property growth be enough to cover costs 1-3?
  5. What will be the payback period (the number of years until you break even on costs 1-3)?

If you rent, you need to make sure to invest (what would have gone to your home deposit) into other areas like: (index/mutual/superannuation) [funds]({{url_for('fund_page')}}), fixed interest (bond or [peer-to-peer]({{url_for('p2p_page')}})) or something else. You might decide to buy at a later date in which case you need to consider the trade-offs, for example:

  * Rent home now and buy home later - more cash to spend to fund your lifestyle in your earlier years but you need to be more diligent with investing elsewhere.
  * Buy home now - less cash to spend now but you have the ability to buy a property closer to the city before prices get too high.

### Calculate it for yourself
For a given set of financial inputs including: capital (the deposit), property price, mortgage rate, estimated property growth, costs, number of years you own the property etc, you can calculate what the return on investment will be for your situation. This number can be easily compared to renting, which is a much simpler calculation. There will be times when renting is better, times when buying is better, or perhaps sometimes the options are indifferent. There’s no universal right or wrong decision. It can be tricky to figure out how to calculate all of this, since it needs maths, domain knowledge and spreadsheets, but fortunately we’ve done a lot of this hard work for you. We've created an [online tool]({{url_for('property_page')}}) to help you make an informed decision. Let’s walk through a case-study calculation...

### Case study - calculation
[The Investment Calculator]({{url_for('login')}}) exists to make investment easier. We think about financial decisions in investment terms so “rent vs buy” is no different (lifestyle considerations aside). Consider the following example (numbers for demo purposes):

{# https://www.pexels.com/photo/portrait-photo-of-smiling-man-with-his-arms-crossed-standing-in-front-of-white-wall-2379004/ #}
<br>
<img src="{{url_for('static', filename='blog/buy-vs-rent-Dennis.jpg')}}" class="center" style="display: block;margin-left:auto;margin-right:auto">
<br>

  * _Dennis wants to buy a property in Hawthorn for **$800k** with an initial deposit of **$160k** on a **25 year** mortgage at **4%** p.a.._
  * _There will also be stamp-duty and other buying costs of **$50k**._
  * _He’s worked out that it will cost him roughly **4%** of the property’s value per year to run (through research like [this](https://www.nerdwallet.com/blog/mortgages/the-real-cost-of-your-house/), [this](https://www.investopedia.com/financial-edge/0412/11-hidden-costs-of-owning-a-home.aspx) or [this](https://www.google.com/search?q=cost+of+owning+a+home))_
  * _He predicts growth in Hawthorn will be **5%** p.a. (through research like [this](https://www.yourinvestmentpropertymag.com.au/top-suburbs/vic-3122-hawthorn.aspx) or [this](https://www.google.com/search?q=property+growth+rate))_
  * _And finally, he plans to own it for **10 years** before selling it, where there will be **$5k** of fixed costs and **3%** commission paid._


_Dennis knows that in his other investments - one or more funds are estimated to earn around **9%** p.a. over the next **10 years**. He wants to know which option is better: buying his home or renting (and instead investing the $160k into the fund)? (For simplicity we consider rent the same amount as mortgage repayments)_

### Case study - results
For this example, using the investment calculator, Dennis’ investment returns would be higher if he rents his home. The initial capital of **$160k** invested would have reached **$379k** for renting (and investing in fund) compared with **$353k** for buying his home and selling after 10 years. 

Interestingly, the answer was close, so if one or more of the inputs above were different, then returns could be higher for buying. For example, if property growth was instead 6%, the final investment value for buying his home would be $457k. There would similarly be changes to the outcome if other inputs were different: buying costs, mortgage, running costs etc. See the chart below to demonstrate this. For property growth between 3% and 7% the final investment results vary significantly!

<img src="{{url_for('static', filename='blog/buy-vs-rent-whatif-plot.PNG')}}" class="center">

For more ‘what if’ charts like this, [calculate buying vs renting your home]({{url_for('property_page')}}) for your own situation.

### Further considerations
The Investment Calculator is a model - a representation of the world to estimate an outcome based on some inputs. No model is perfect, however some models are useful which I hope is the case for you. We are not a registered financial authority, so please use this as a tool to aid your research but do not take it as an investment advice. Here are some of the caveats to consider:

  * The monthly running costs of owning a home are included within the investment calculation - having this cost as a % of the current property value may be a good way to model running costs but there could be better techniques.
  * There’s no discount rate for inflation in the costs of buying, running and selling the property. For example, $10k now is not the same as 10k in 10 years time, perhaps this would change the outcome in some cases.
  * This model does not compare the benefits in taxation between either option. For example when selling shares there are capital gains taxes which are often not paid for an owner occupied property that is sold.
  * We assume for simplicity that the monthly mortgage repayments are the same as rental payments. In reality either one could be a lower amount which would allow more ability to invest in other areas.

Let us know your thoughts. For other investment decisions, see all calculators [here]({{url_for('index')}}).

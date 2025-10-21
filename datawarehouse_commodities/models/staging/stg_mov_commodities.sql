-- import
with source as (

    select 
        date,
        symbol,
        action,
        quantity
    from {{source ('PipelineCommodities','mov_commodities')}}
),
-- renamed

renamed as (


    select 
        cast(date as date) as data,
        symbol as simbolo,
        action as acao,
        quantity as quantidade
        
    from
        source

)

-- select * from

select * from renamed
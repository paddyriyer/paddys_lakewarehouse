import { useState, useEffect } from "react";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Treemap } from "recharts";

// ═══ THEME ═══
const C = {bg:"#F8FAFC",panel:"#FFFFFF",card:"#FFFFFF",card2:"#F1F5F9",border:"#E2E8F0",text:"#1E293B",muted:"#64748B",dim:"#94A3B8",
  accent:"#FF9900",green:"#10B981",red:"#EF4444",purple:"#8B5CF6",blue:"#3B82F6",cyan:"#06B6D4",gold:"#F59E0B",pink:"#EC4899",lime:"#84CC16",teal:"#14B8A6"};
const PAL = [C.accent,C.purple,C.cyan,C.green,C.gold,C.blue,C.red,C.pink,C.lime,C.teal];
const ttStyle = {background:"#FFFFFF",border:"1px solid #E2E8F0",boxShadow:"0 1px 3px rgba(0,0,0,0.08)",borderRadius:8,fontSize:11,color:C.text};

// ═══ DATA ═══
const monthly = [{m:"Jan'24",rev:484.8,profit:267.4,o:169},{m:"Feb",rev:392,profit:165.8,o:147},{m:"Mar",rev:380.1,profit:206.2,o:133},{m:"Apr",rev:361.3,profit:142.4,o:141},{m:"May",rev:450.8,profit:209.8,o:157},{m:"Jun",rev:346.1,profit:163.2,o:126},{m:"Jul",rev:450.1,profit:228.3,o:149},{m:"Aug",rev:434,profit:226.7,o:144},{m:"Sep",rev:410.8,profit:194.2,o:153},{m:"Oct",rev:364,profit:168.1,o:140},{m:"Nov",rev:360,profit:169.9,o:132},{m:"Dec'24",rev:391.2,profit:175.6,o:143},{m:"Jan'25",rev:441.2,profit:233,o:145},{m:"Feb",rev:343.1,profit:164.9,o:126},{m:"Mar",rev:417.5,profit:199.4,o:151},{m:"Apr",rev:395.2,profit:202.9,o:135},{m:"May",rev:397.9,profit:203.1,o:146},{m:"Jun",rev:389,profit:195.6,o:130},{m:"Jul",rev:381.4,profit:191,o:138},{m:"Aug",rev:418.4,profit:204.4,o:159},{m:"Sep",rev:396,profit:189.4,o:133},{m:"Oct",rev:375.9,profit:198.1,o:131},{m:"Nov",rev:341.1,profit:154.9,o:115},{m:"Dec'25",rev:401.9,profit:241.5,o:117},{m:"Jan'26",rev:379.3,profit:176.2,o:140}];
const segments = [{name:"Mid-Market",rev:2796.9,cust:142},{name:"Startup",rev:2615.4,cust:129},{name:"SMB",rev:2412.6,cust:120},{name:"Enterprise",rev:2078.1,cust:107}];
const countries = [{c:"US",rev:2883.1,cust:142},{c:"UK",rev:1277.1,cust:65},{c:"JP",rev:883.9,cust:43},{c:"DE",rev:847.5,cust:43},{c:"FR",rev:829.8,cust:42},{c:"SG",rev:794.1,cust:41},{c:"AU",rev:671.5,cust:34},{c:"IN",rev:598,cust:28},{c:"BR",rev:589.1,cust:32},{c:"CA",rev:528.7,cust:28}];
const categories = [{name:"Hardware",rev:1522.3},{name:"Security",rev:1358.5},{name:"Analytics",rev:1346.3},{name:"Support",rev:1338},{name:"Cloud",rev:1209.5},{name:"Training",rev:1194.1},{name:"Services",rev:1072.2},{name:"License",rev:862}];
const lcStages = [{name:"Dormant",value:231,color:"#6B7280"},{name:"Activated",value:70,color:C.blue},{name:"At-Risk",value:69,color:C.gold},{name:"Champion",value:68,color:C.green},{name:"Churned",value:53,color:C.red},{name:"Loyal",value:9,color:C.purple}];
const churnTiers = [{name:"High",value:313,color:C.red},{name:"Low",value:130,color:C.green},{name:"Medium",value:57,color:C.gold}];
const pipeline = [{stage:"Lead",deals:70,val:38.6},{stage:"MQL",deals:152,val:87.2},{stage:"SQL",deals:197,val:108.5},{stage:"Discovery",deals:211,val:101.4},{stage:"Proposal",deals:178,val:89.3},{stage:"Negotiation",deals:169,val:91},{stage:"Won",deals:133,val:69.7},{stage:"Lost",deals:90,val:39.9}];
const reps = [{r:"Rep 12",deals:50,won:11,wr:84.6,pipe:25.7},{r:"Rep 19",deals:52,won:9,wr:81.8,pipe:27.7},{r:"Rep 1",deals:49,won:8,wr:80,pipe:17.6},{r:"Rep 5",deals:50,won:6,wr:75,pipe:33.8},{r:"Rep 3",deals:48,won:8,wr:72.7,pipe:23.4},{r:"Rep 2",deals:54,won:9,wr:64.3,pipe:26.4},{r:"Rep 10",deals:51,won:8,wr:57.1,pipe:23.3},{r:"Rep 17",deals:46,won:6,wr:54.5,pipe:29.8}];
const leadSources = [{s:"Product-Led",deals:161,won:22,wr:13.7},{s:"Existing Customer",deals:136,won:18,wr:13.2},{s:"Content Download",deals:146,won:18,wr:12.3},{s:"Partner Referral",deals:146,won:18,wr:12.3},{s:"Inbound Web",deals:149,won:16,wr:10.7},{s:"Outbound SDR",deals:134,won:14,wr:10.4},{s:"Paid Campaign",deals:167,won:16,wr:9.6},{s:"Event/Conference",deals:161,won:11,wr:6.8}];
const lossReasons = [{reason:"Price",count:22},{reason:"Feature Gap",count:21},{reason:"No Decision",count:19},{reason:"Timing",count:15},{reason:"Competition",count:13}];
const fraudSev = [{name:"Medium",value:207,color:C.gold},{name:"Low",value:157,color:C.green},{name:"High",value:75,color:C.red},{name:"Critical",value:11,color:"#B91C1C"}];
const fraudStatus = [{name:"False Positive",value:134,color:"#6B7280"},{name:"Resolved",value:126,color:C.green},{name:"Investigating",value:86,color:C.gold},{name:"Confirmed",value:56,color:C.red},{name:"Open",value:48,color:C.blue}];
const fraudTypes = [{type:"Split Txn",count:47},{type:"Round Amt",count:43},{type:"After-Hrs",count:41},{type:"Phantom Vendor",count:38},{type:"Geo Mismatch",count:38},{type:"PO Mismatch",count:37},{type:"Amount Spike",count:36},{type:"ID Mismatch",count:36}];
const detMethods = [{method:"Pattern Match",count:98},{method:"ML Anomaly",count:92},{method:"Claude AI",count:89},{method:"Manual",count:86},{method:"Rule-Based",count:85}];
const rtData = [{h:"09:00",users:436,pv:2922,api:16132,ms:160},{h:"10:00",users:473,pv:3529,api:22209,ms:218},{h:"11:00",users:719,pv:3679,api:23513,ms:191},{h:"12:00",users:834,pv:3422,api:24605,ms:187},{h:"13:00",users:808,pv:3548,api:27508,ms:254},{h:"14:00",users:582,pv:2251,api:16744,ms:140},{h:"15:00",users:755,pv:3188,api:24396,ms:157},{h:"16:00",users:399,pv:3650,api:22101,ms:215},{h:"17:00",users:902,pv:2998,api:31894,ms:150}];
const funnelData = [{step:"Homepage",val:1348,pct:100},{step:"Products",val:1408,pct:104},{step:"Pricing",val:1402,pct:104},{step:"Demo Req",val:1420,pct:105},{step:"Checkout",val:1358,pct:101}];
const referrers = [{src:"Email",conv:5.53,visits:2621},{src:"Paid LinkedIn",conv:5.78,visits:2508},{src:"Bing",conv:5.82,visits:2561},{src:"Organic Social",conv:5.55,visits:2433},{src:"Google",conv:5.29,visits:2477},{src:"Direct",conv:5.09,visits:2552},{src:"LinkedIn",conv:5.14,visits:2527},{src:"Partner",conv:4.73,visits:2493}];
const mdmMatch = [{name:"AUTO_MERGE",value:117,color:C.green},{name:"REVIEW",value:53,color:C.gold},{name:"NO_MATCH",value:30,color:C.red}];
const sourceLink = [{name:"SAP+SFDC+Oracle",value:94},{name:"SAP+Salesforce",value:93},{name:"SAP only",value:83},{name:"SFDC+Oracle",value:82},{name:"Salesforce only",value:75},{name:"SAP+Oracle",value:73}];

// ═══ COMPONENTS ═══
const KPI = ({label,value,sub,color=C.accent,trend,icon=""}) => (
  <div style={{background:C.card,borderRadius:10,padding:"14px 16px",border:"1px solid #E2E8F0",boxShadow:"0 1px 3px rgba(0,0,0,0.08)",flex:1,minWidth:130,position:"relative",overflow:"hidden"}}>
    <div style={{position:"absolute",top:0,left:0,width:"100%",height:2.5,background:color}}/>
    <div style={{fontSize:10,color:C.muted,fontWeight:600,letterSpacing:.5,textTransform:"uppercase",marginBottom:2}}>{icon} {label}</div>
    <div style={{fontSize:24,fontWeight:800,color,fontFamily:"'DM Sans',sans-serif"}}>{value}</div>
    {sub && <div style={{fontSize:10,color:C.dim,marginTop:2}}>{sub}</div>}
    {trend && <span style={{fontSize:10,color:trend>0?C.green:C.red,fontWeight:600}}>{trend>0?"▲":"▼"} {Math.abs(trend)}%</span>}
  </div>
);

const Card = ({title,children,span=1,h}) => (
  <div style={{background:C.card,borderRadius:10,border:"1px solid #E2E8F0",boxShadow:"0 1px 3px rgba(0,0,0,0.08)",padding:"14px 16px",gridColumn:`span ${span}`,display:"flex",flexDirection:"column",minHeight:h||"auto"}}>
    <div style={{fontSize:12,fontWeight:700,color:C.text,marginBottom:10,letterSpacing:.3}}>{title}</div>
    <div style={{flex:1,minHeight:0}}>{children}</div>
  </div>
);

const Pill = ({text,color}) => <span style={{background:`${color}22`,color,padding:"2px 8px",borderRadius:4,fontSize:10,fontWeight:600}}>{text}</span>;

const StatusDot = ({color,pulse}) => (
  <span style={{display:"inline-block",width:8,height:8,borderRadius:"50%",background:color,marginRight:6,
    animation:pulse?"pulse 2s infinite":"none"}}/>
);

const tabs = ["⚡ Executive RT","📊 Revenue","👥 Customer 360","🔄 Lifecycle","🎯 GTM Pipeline","🖱️ Clickstream","🛡️ Fraud","🔗 MDM & DQ"];

export default function Dashboard() {
  const [tab, setTab] = useState(0);
  const [now, setNow] = useState(new Date());
  useEffect(()=>{const t=setInterval(()=>setNow(new Date()),1000);return()=>clearInterval(t);},[]);

  return (
    <div style={{background:C.bg,minHeight:"100vh",fontFamily:"'DM Sans',-apple-system,sans-serif",color:C.text}}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
      <style>{`@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}} ::-webkit-scrollbar{width:6px;height:6px} ::-webkit-scrollbar-thumb{background:#2A3A50;border-radius:3px}`}</style>

      {/* Header */}
      <div style={{background:"#FFFFFF",borderBottom:`1px solid ${C.border}`,padding:"10px 20px",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
        <div style={{display:"flex",alignItems:"center",gap:12}}>
          <div style={{width:32,height:32,borderRadius:8,background:"linear-gradient(135deg,#FF9900,#8B5CF6)",display:"flex",alignItems:"center",justifyContent:"center",fontWeight:800,fontSize:14,color:"#FFFFFF"}}>S</div>
          <div>
            <div style={{fontSize:14,fontWeight:800}}>Enterprise MDM Lakehouse — Full Analytics</div>
            <div style={{fontSize:10,color:C.muted}}>Claude Opus 4.6 • 11 Tables • 36,650 Records • S3 + Delta + Snowflake</div>
          </div>
        </div>
        <div style={{display:"flex",alignItems:"center",gap:16}}>
          <div style={{textAlign:"right"}}>
            <div style={{fontSize:10,color:C.muted}}>
              <StatusDot color={C.green} pulse/> LIVE — {now.toLocaleTimeString()}
            </div>
            <div style={{fontSize:9,color:C.dim}}>Uptime: 99.95% | DQ: 97.5% pass</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{display:"flex",gap:0,padding:"0 12px",background:"#FFFFFF",borderBottom:`1px solid ${C.border}`,overflowX:"auto"}}>
        {tabs.map((t,i)=>(
          <button key={i} onClick={()=>setTab(i)} style={{
            padding:"9px 14px",fontSize:11,fontWeight:tab===i?700:500,whiteSpace:"nowrap",
            color:tab===i?C.accent:C.muted,background:"transparent",border:"none",
            borderBottom:tab===i?`2px solid ${C.accent}`:"2px solid transparent",
            cursor:"pointer",fontFamily:"inherit"
          }}>{t}</button>
        ))}
      </div>

      <div style={{padding:16,maxWidth:1440,margin:"0 auto"}}>
        {tab===0&&<ExecRT now={now}/>}{tab===1&&<Revenue/>}{tab===2&&<Cust360/>}{tab===3&&<Lifecycle/>}
        {tab===4&&<GTM/>}{tab===5&&<Clickstream/>}{tab===6&&<Fraud/>}{tab===7&&<MDM/>}
      </div>
    </div>
  );
}

// ═══ TAB 0: EXECUTIVE REAL-TIME ═══
function ExecRT({now}) {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10,flexWrap:"wrap"}}>
      <KPI icon="👁️" label="Active Users Now" value="834" sub="Peak: 902 at 17:00" color={C.cyan} trend={12}/>
      <KPI icon="📈" label="Revenue Today" value="$8.2M" sub="3 deals closed" color={C.accent} trend={5}/>
      <KPI icon="🎯" label="Pipeline Value" value="$516M" sub="977 open deals" color={C.purple}/>
      <KPI icon="🚀" label="New Leads Today" value="47" sub="Product-Led: 22" color={C.green} trend={18}/>
      <KPI icon="⚡" label="API Latency" value="180ms" sub="P99: 420ms" color={C.blue}/>
      <KPI icon="🛡️" label="Fraud Alerts" value="48 open" sub="11 critical" color={C.red}/>
      <KPI icon="✅" label="DQ Pass Rate" value="97.5%" sub="All layers" color={C.teal}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"2fr 1fr",gap:12}}>
      <Card title="📊 Real-Time Traffic — Today (Hourly)">
        <ResponsiveContainer width="100%" height={240}>
          <ComposedChart data={rtData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/>
            <XAxis dataKey="h" tick={{fill:"#64748B",fontSize:10}}/>
            <YAxis tick={{fill:"#64748B",fontSize:10}}/>
            <YAxis yAxisId="r" orientation="right" tick={{fill:"#64748B",fontSize:9}}/>
            <Tooltip contentStyle={ttStyle}/>
            <Area type="monotone" dataKey="users" fill={`${C.cyan}30`} stroke={C.cyan} strokeWidth={2} name="Active Users"/>
            <Line type="monotone" dataKey="ms" stroke={C.gold} strokeWidth={1.5} dot={false} yAxisId="r" name="Latency (ms)"/>
          </ComposedChart>
        </ResponsiveContainer>
      </Card>
      <Card title="🏢 Revenue by Segment ($M)">
        <ResponsiveContainer width="100%" height={240}>
          <PieChart><Pie data={segments} cx="50%" cy="50%" innerRadius={50} outerRadius={85} dataKey="rev" label={({name,percent,cx,cy,midAngle,outerRadius,index})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:9,fontWeight:600},`${name} ${(percent*100).toFixed(0)}%`)}}>
            {segments.map((e,i)=><Cell key={i} fill={PAL[i]}/>)}
          </Pie><Tooltip contentStyle={ttStyle}/></PieChart>
        </ResponsiveContainer>
      </Card>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:12}}>
      <Card title="🔗 Pipeline Funnel">
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={pipeline} layout="vertical" margin={{left:15}}>
            <XAxis type="number" tick={{fill:"#64748B",fontSize:9}}/>
            <YAxis type="category" dataKey="stage" tick={{fill:"#64748B",fontSize:9}} width={65}/>
            <Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="deals" name="Deals" radius={[0,4,4,0]}>
              {pipeline.map((e,i)=><Cell key={i} fill={e.stage==="Won"?C.green:e.stage==="Lost"?C.red:PAL[i%8]}/>)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
      <Card title="🛡️ Fraud by Severity">
        <ResponsiveContainer width="100%" height={200}>
          <PieChart><Pie data={fraudSev} cx="50%" cy="50%" innerRadius={40} outerRadius={70} dataKey="value" label={({name,value,cx,cy,midAngle,outerRadius})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:9,fontWeight:600},`${name}: ${value}`)}}>
            {fraudSev.map((e,i)=><Cell key={i} fill={e.color}/>)}
          </Pie><Tooltip contentStyle={ttStyle}/></PieChart>
        </ResponsiveContainer>
      </Card>
      <Card title="👥 Lifecycle Stage Distribution">
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={lcStages}>
            <XAxis dataKey="name" tick={{fill:"#64748B",fontSize:9}}/>
            <YAxis tick={{fill:"#64748B",fontSize:9}}/>
            <Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="value" name="Customers" radius={[4,4,0,0]}>
              {lcStages.map((e,i)=><Cell key={i} fill={e.color}/>)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  </div>);
}

// ═══ TAB 1: REVENUE ═══
function Revenue() {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="💰" label="Revenue" value="$9.90B" color={C.accent}/><KPI icon="📈" label="Profit" value="$4.87B" color={C.green}/>
      <KPI icon="📊" label="Margin" value="49.2%" color={C.cyan}/><KPI icon="🛒" label="Orders" value="3,500" color={C.blue}/><KPI icon="📏" label="AOV" value="$2.83M" color={C.gold}/>
    </div>
    <Card title="📊 Monthly Revenue & Profit ($M)">
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={monthly}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="m" tick={{fill:"#64748B",fontSize:8}} interval={2}/>
          <YAxis tick={{fill:"#64748B",fontSize:9}}/><Tooltip contentStyle={ttStyle}/><Legend wrapperStyle={{fontSize:10}}/>
          <Bar dataKey="rev" fill={C.accent} name="Revenue" opacity={.8} radius={[3,3,0,0]}/><Bar dataKey="profit" fill={C.green} name="Profit" opacity={.8} radius={[3,3,0,0]}/>
        </ComposedChart>
      </ResponsiveContainer>
    </Card>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
      <Card title="📦 Revenue by Category ($M)">
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={categories} layout="vertical" margin={{left:15}}><XAxis type="number" tick={{fill:"#64748B",fontSize:9}}/><YAxis type="category" dataKey="name" tick={{fill:"#64748B",fontSize:9}} width={65}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="rev" name="Revenue" radius={[0,4,4,0]}>{categories.map((e,i)=><Cell key={i} fill={PAL[i]}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
      <Card title="🌍 Revenue by Country ($M)">
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={countries}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="c" tick={{fill:"#64748B",fontSize:9}}/><YAxis tick={{fill:"#64748B",fontSize:9}}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="rev" name="Revenue" radius={[4,4,0,0]}>{countries.map((e,i)=><Cell key={i} fill={PAL[i%10]}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  </div>);
}

// ═══ TAB 2: CUSTOMER 360 ═══
function Cust360() {
  const statusData = [{name:"Active",value:311,color:C.green},{name:"New",value:70,color:C.cyan},{name:"At-Risk",value:66,color:C.gold},{name:"Churned",value:53,color:C.red}];
  const sentimentData = [{name:"Positive",value:3063,color:C.green},{name:"Neutral",value:2006,color:"#94A3B8"},{name:"Negative",value:931,color:C.red}];
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="👥" label="Golden Records" value="500" color={C.purple}/><KPI icon="✅" label="Active" value="311" sub="62.2%" color={C.green}/>
      <KPI icon="⚠️" label="At-Risk" value="66" color={C.gold}/><KPI icon="❌" label="Churned" value="53" color={C.red}/><KPI icon="🔁" label="Repeat Rate" value="94.0%" color={C.cyan}/>
      <KPI icon="💬" label="Interactions" value="6,000" sub="51% positive" color={C.blue}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:12}}>
      <Card title="👥 Customer Status"><ResponsiveContainer width="100%" height={200}><PieChart><Pie data={statusData} cx="50%" cy="50%" innerRadius={45} outerRadius={75} dataKey="value" label={({name,percent,cx,cy,midAngle,outerRadius,index})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:9,fontWeight:600},`${name} ${(percent*100).toFixed(0)}%`)}}>{statusData.map((e,i)=><Cell key={i} fill={e.color}/>)}</Pie><Tooltip contentStyle={ttStyle}/></PieChart></ResponsiveContainer></Card>
      <Card title="💬 Sentiment"><ResponsiveContainer width="100%" height={200}><PieChart><Pie data={sentimentData} cx="50%" cy="50%" innerRadius={45} outerRadius={75} dataKey="value" label={({name,percent,cx,cy,midAngle,outerRadius,index})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:9,fontWeight:600},`${name} ${(percent*100).toFixed(0)}%`)}}>{sentimentData.map((e,i)=><Cell key={i} fill={e.color}/>)}</Pie><Tooltip contentStyle={ttStyle}/></PieChart></ResponsiveContainer></Card>
      <Card title="🏢 Revenue by Segment"><ResponsiveContainer width="100%" height={200}><RadarChart data={segments} cx="50%" cy="50%" outerRadius={60}><PolarGrid stroke="#E2E8F0"/><PolarAngleAxis dataKey="name" tick={{fill:"#64748B",fontSize:9}}/><Radar dataKey="rev" stroke={C.accent} fill={C.accent} fillOpacity={.3}/><Radar dataKey="cust" stroke={C.purple} fill={C.purple} fillOpacity={.2}/><Tooltip contentStyle={ttStyle}/></RadarChart></ResponsiveContainer></Card>
    </div>
  </div>);
}

// ═══ TAB 3: LIFECYCLE ═══
function Lifecycle() {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="🏆" label="Champions" value="68" sub="Tenure 24+ months" color={C.green}/>
      <KPI icon="💤" label="Dormant" value="231" sub="No activity 90+ days" color="#6B7280"/>
      <KPI icon="⚠️" label="At-Risk" value="69" sub="45-90 day gap" color={C.gold}/>
      <KPI icon="🆕" label="Onboarding" value="70" sub="< 3 months tenure" color={C.cyan}/>
      <KPI icon="❌" label="Churned" value="53" sub="Lost customers" color={C.red}/>
      <KPI icon="🔁" label="Repeat Rate" value="94.0%" color={C.purple}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
      <Card title="🔄 Lifecycle Stage Distribution">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={lcStages}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="name" tick={{fill:"#64748B",fontSize:10}}/><YAxis tick={{fill:"#64748B",fontSize:10}}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="value" name="Customers" radius={[4,4,0,0]}>{lcStages.map((e,i)=><Cell key={i} fill={e.color}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
      <Card title="🎯 Churn Risk Tiers">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart><Pie data={churnTiers} cx="50%" cy="50%" innerRadius={55} outerRadius={95} dataKey="value" label={({name,value,cx,cy,midAngle,outerRadius})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:10,fontWeight:600},`${name}: ${value}`)}}>{churnTiers.map((e,i)=><Cell key={i} fill={e.color}/>)}</Pie><Tooltip contentStyle={ttStyle}/></PieChart>
        </ResponsiveContainer>
      </Card>
    </div>
    <Card title="📋 Lifecycle Stage Definitions & Actions">
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10}}>
        {[{stage:"Champion",color:C.green,tenure:"24+ mo",desc:"Highest LTV, lowest churn risk. Upsell opportunities.",action:"VIP programs, case studies, referral incentives"},
          {stage:"Loyal",color:C.purple,tenure:"12-24 mo",desc:"Consistent buyers, good health. Expansion candidates.",action:"Cross-sell, feature adoption, NPS surveys"},
          {stage:"Growing",color:C.blue,tenure:"3-12 mo",desc:"Active engagement, building relationship.",action:"Onboarding complete, product training, success plans"},
          {stage:"At-Risk",color:C.gold,tenure:"45-90d gap",desc:"Engagement declining. Intervention needed.",action:"CSM outreach, health check, incentive offers"},
          {stage:"Dormant",color:"#6B7280",tenure:"90+ day gap",desc:"No recent activity. Reactivation campaigns.",action:"Win-back emails, special offers, executive outreach"},
          {stage:"Churned",color:C.red,tenure:"Cancelled",desc:"Lost customer. Post-mortem analysis.",action:"Exit surveys, loss analysis, future re-engagement"}
        ].map((s,i)=>(
          <div key={i} style={{background:C.card2,borderRadius:8,padding:12,borderLeft:`3px solid ${s.color}`}}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:6}}>
              <span style={{fontWeight:700,color:s.color,fontSize:13}}>{s.stage}</span>
              <Pill text={s.tenure} color={s.color}/>
            </div>
            <div style={{fontSize:10,color:C.text,marginBottom:4}}>{s.desc}</div>
            <div style={{fontSize:9,color:C.muted}}>→ {s.action}</div>
          </div>
        ))}
      </div>
    </Card>
  </div>);
}

// ═══ TAB 4: GTM PIPELINE ═══
function GTM() {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="🎯" label="Total Deals" value="1,200" color={C.purple}/><KPI icon="✅" label="Won" value="133" sub="$69.7M" color={C.green}/>
      <KPI icon="❌" label="Lost" value="90" sub="$39.9M" color={C.red}/><KPI icon="📊" label="Win Rate" value="59.6%" color={C.accent}/>
      <KPI icon="💰" label="Open Pipeline" value="$516M" sub="977 deals" color={C.cyan}/><KPI icon="🏃" label="Avg Cycle" value="92 days" color={C.gold}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"2fr 1fr",gap:12}}>
      <Card title="🔗 Pipeline Funnel — Deals by Stage">
        <ResponsiveContainer width="100%" height={260}>
          <ComposedChart data={pipeline}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="stage" tick={{fill:"#64748B",fontSize:9}}/><YAxis tick={{fill:"#64748B",fontSize:9}}/><YAxis yAxisId="r" orientation="right" tick={{fill:"#64748B",fontSize:9}}/><Tooltip contentStyle={ttStyle}/><Legend wrapperStyle={{fontSize:10}}/>
            <Bar dataKey="deals" name="Deals" radius={[4,4,0,0]}>{pipeline.map((e,i)=><Cell key={i} fill={e.stage==="Won"?C.green:e.stage==="Lost"?C.red:PAL[i%8]}/>)}</Bar>
            <Line type="monotone" dataKey="val" stroke={C.accent} strokeWidth={2} yAxisId="r" name="Value $M" dot/>
          </ComposedChart>
        </ResponsiveContainer>
      </Card>
      <Card title="❌ Loss Reasons">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={lossReasons} layout="vertical" margin={{left:15}}><XAxis type="number" tick={{fill:"#64748B",fontSize:9}}/><YAxis type="category" dataKey="reason" tick={{fill:"#64748B",fontSize:10}} width={80}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="count" name="Lost Deals" fill={C.red} radius={[0,4,4,0]}/>
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
      <Card title="🏆 Top Sales Reps by Win Rate">
        <table style={{width:"100%",borderCollapse:"collapse",fontSize:11}}>
          <thead><tr>{["Rep","Deals","Won","Win Rate","Pipeline $M"].map((h,i)=><th key={i} style={{padding:"6px 10px",textAlign:i>=2?"right":"left",color:C.muted,borderBottom:`1px solid ${C.border}`,fontSize:10}}>{h}</th>)}</tr></thead>
          <tbody>{reps.map((r,i)=>(
            <tr key={i} style={{borderBottom:`1px solid ${C.border}22`}}>
              <td style={{padding:"6px 10px",fontWeight:600}}>{r.r}</td>
              <td style={{padding:"6px 10px",textAlign:"right"}}>{r.deals}</td>
              <td style={{padding:"6px 10px",textAlign:"right",fontWeight:700,color:C.green}}>{r.won}</td>
              <td style={{padding:"6px 10px",textAlign:"right"}}><div style={{display:"flex",alignItems:"center",justifyContent:"flex-end",gap:6}}><div style={{width:50,height:5,background:C.border,borderRadius:3}}><div style={{width:`${r.wr}%`,height:"100%",background:r.wr>=70?C.green:r.wr>=55?C.gold:C.red,borderRadius:3}}/></div>{r.wr}%</div></td>
              <td style={{padding:"6px 10px",textAlign:"right",color:C.accent}}>${r.pipe}M</td>
            </tr>
          ))}</tbody>
        </table>
      </Card>
      <Card title="📡 Lead Source Performance">
        <ResponsiveContainer width="100%" height={230}>
          <BarChart data={leadSources} layout="vertical" margin={{left:20}}><XAxis type="number" tick={{fill:"#64748B",fontSize:9}}/><YAxis type="category" dataKey="s" tick={{fill:"#64748B",fontSize:9}} width={100}/><Tooltip contentStyle={ttStyle}/><Legend wrapperStyle={{fontSize:10}}/>
            <Bar dataKey="won" name="Won" fill={C.green} stackId="a" radius={[0,0,0,0]}/>
            <Bar dataKey="deals" name="Total Deals" fill={`${C.blue}40`} radius={[0,4,4,0]}/>
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  </div>);
}

// ═══ TAB 5: CLICKSTREAM ═══
function Clickstream() {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="🖱️" label="Total Events" value="25,000" color={C.cyan}/><KPI icon="🔄" label="Conversions" value="1,342" sub="5.4% rate" color={C.green}/>
      <KPI icon="📱" label="Sessions" value="8,000" color={C.purple}/><KPI icon="🌐" label="Unique Visitors" value="2,000" sub="Anonymous: 30%" color={C.blue}/>
      <KPI icon="🏷️" label="Top Referrer" value="Email" sub="5.53% conv rate" color={C.accent}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
      <Card title="🔗 Conversion Funnel — Page Views">
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={funnelData}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="step" tick={{fill:"#64748B",fontSize:10}}/><YAxis tick={{fill:"#64748B",fontSize:10}}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="val" name="Visitors" radius={[4,4,0,0]}>{funnelData.map((e,i)=><Cell key={i} fill={PAL[i]}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
      <Card title="📡 Referrer Source — Visits & Conversion Rate">
        <ResponsiveContainer width="100%" height={240}>
          <ComposedChart data={referrers}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="src" tick={{fill:"#64748B",fontSize:9}}/><YAxis tick={{fill:"#64748B",fontSize:9}}/><YAxis yAxisId="r" orientation="right" tick={{fill:"#64748B",fontSize:9}} domain={[4,7]}/><Tooltip contentStyle={ttStyle}/><Legend wrapperStyle={{fontSize:10}}/>
            <Bar dataKey="visits" name="Visits" fill={`${C.blue}60`} radius={[3,3,0,0]}/>
            <Line type="monotone" dataKey="conv" stroke={C.green} strokeWidth={2} yAxisId="r" name="Conv %" dot/>
          </ComposedChart>
        </ResponsiveContainer>
      </Card>
    </div>
    <Card title="📋 Attribution Model — UTM Campaign Performance">
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10}}>
        {[{camp:"spring_launch",leads:180,conv:8.2,color:C.green},{camp:"q4_push",leads:165,conv:7.1,color:C.accent},
          {camp:"partner_webinar",leads:142,conv:6.8,color:C.purple},{camp:"product_update",leads:130,conv:5.9,color:C.blue},
          {camp:"brand_awareness",leads:120,conv:4.2,color:C.cyan},{camp:"retarget_q1",leads:155,conv:9.1,color:C.gold}
        ].map((c,i)=>(
          <div key={i} style={{background:C.card2,borderRadius:8,padding:12,borderTop:`3px solid ${c.color}`}}>
            <div style={{fontSize:12,fontWeight:700,color:c.color}}>{c.camp}</div>
            <div style={{fontSize:20,fontWeight:800,color:C.text,margin:"4px 0"}}>{c.conv}%</div>
            <div style={{fontSize:10,color:C.muted}}>Conversion Rate • {c.leads} leads</div>
          </div>
        ))}
      </div>
    </Card>
  </div>);
}

// ═══ TAB 6: FRAUD ═══
function Fraud() {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="🛡️" label="Total Alerts" value="450" color={C.red}/><KPI icon="🚨" label="Critical" value="11" color="#B91C1C"/>
      <KPI icon="✅" label="Confirmed Fraud" value="56" sub="$609K impact" color={C.red}/><KPI icon="❎" label="False Positive" value="134" sub="29.8% FP rate" color="#6B7280"/>
      <KPI icon="🔍" label="Investigating" value="86" color={C.gold}/><KPI icon="🤖" label="AI Detected" value="89" sub="Claude AI Analysis" color={C.purple}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:12}}>
      <Card title="🔴 Severity Distribution">
        <ResponsiveContainer width="100%" height={220}><PieChart><Pie data={fraudSev} cx="50%" cy="50%" innerRadius={45} outerRadius={80} dataKey="value" label={({name,value,cx,cy,midAngle,outerRadius})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:10,fontWeight:600},`${name}: ${value}`)}}>{fraudSev.map((e,i)=><Cell key={i} fill={e.color}/>)}</Pie><Tooltip contentStyle={ttStyle}/></PieChart></ResponsiveContainer>
      </Card>
      <Card title="📊 Alert Status">
        <ResponsiveContainer width="100%" height={220}><PieChart><Pie data={fraudStatus} cx="50%" cy="50%" innerRadius={45} outerRadius={80} dataKey="value" label={({name,value,cx,cy,midAngle,outerRadius})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:9,fontWeight:600},`${name}: ${value}`)}}>{fraudStatus.map((e,i)=><Cell key={i} fill={e.color}/>)}</Pie><Tooltip contentStyle={ttStyle}/></PieChart></ResponsiveContainer>
      </Card>
      <Card title="🤖 Detection Methods">
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={detMethods} layout="vertical" margin={{left:10}}><XAxis type="number" tick={{fill:"#64748B",fontSize:9}}/><YAxis type="category" dataKey="method" tick={{fill:"#64748B",fontSize:9}} width={85}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="count" name="Alerts" radius={[0,4,4,0]}>{detMethods.map((e,i)=><Cell key={i} fill={PAL[i]}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"2fr 1fr",gap:12}}>
      <Card title="🏷️ Fraud Types — Alert Distribution">
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={fraudTypes}><CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0"/><XAxis dataKey="type" tick={{fill:"#64748B",fontSize:9}}/><YAxis tick={{fill:"#64748B",fontSize:9}}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="count" name="Alerts" radius={[4,4,0,0]}>{fraudTypes.map((e,i)=><Cell key={i} fill={PAL[i%8]}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
      <Card title="🚨 Active Critical Alerts">
        <div style={{display:"flex",flexDirection:"column",gap:8}}>
          {[{id:"FRD-00234",type:"Phantom Vendor",amt:"$487K",risk:95,sys:"SAP"},{id:"FRD-00412",type:"Geo Mismatch",amt:"$123K",risk:92,sys:"Payment"},
            {id:"FRD-00089",type:"Amount Spike",amt:"$1.2M",risk:89,sys:"Oracle"},{id:"FRD-00445",type:"Split Txn",amt:"$67K",risk:87,sys:"E-Commerce"}
          ].map((a,i)=>(
            <div key={i} style={{background:C.card2,borderRadius:6,padding:10,borderLeft:`3px solid ${C.red}`}}>
              <div style={{display:"flex",justifyContent:"space-between"}}>
                <span style={{fontWeight:700,fontSize:11,color:C.text}}>{a.id}</span>
                <Pill text={`Risk: ${a.risk}`} color={C.red}/>
              </div>
              <div style={{fontSize:10,color:C.muted,marginTop:2}}>{a.type} • {a.amt} • {a.sys}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  </div>);
}

// ═══ TAB 7: MDM & DATA QUALITY ═══
function MDM() {
  return (<div style={{display:"flex",flexDirection:"column",gap:14}}>
    <div style={{display:"flex",gap:10}}>
      <KPI icon="🔗" label="Match Pairs" value="200" color={C.purple}/><KPI icon="✅" label="Auto-Merged" value="117" sub="58.5%" color={C.green}/>
      <KPI icon="👁️" label="Review Queue" value="53" color={C.gold}/><KPI icon="🏷️" label="Multi-Source" value="94" sub="3-system linked" color={C.cyan}/>
      <KPI icon="✅" label="DQ Pass Rate" value="97.5%" color={C.teal}/><KPI icon="📊" label="Tables" value="11" sub="36,650 rows total" color={C.blue}/>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
      <Card title="🔗 MDM Match Tier Distribution">
        <ResponsiveContainer width="100%" height={240}><PieChart><Pie data={mdmMatch} cx="50%" cy="50%" innerRadius={55} outerRadius={90} dataKey="value" label={({name,value,cx,cy,midAngle,outerRadius})=>{const RADIAN=Math.PI/180;const r=outerRadius+18;const x=cx+r*Math.cos(-midAngle*RADIAN);const y=cy+r*Math.sin(-midAngle*RADIAN);return React.createElement('text',{x,y,fill:'#E2E8F0',textAnchor:x>cx?'start':'end',dominantBaseline:'central',fontSize:10,fontWeight:600},`${name}: ${value}`)}}>{mdmMatch.map((e,i)=><Cell key={i} fill={e.color}/>)}</Pie><Tooltip contentStyle={ttStyle}/></PieChart></ResponsiveContainer>
      </Card>
      <Card title="🏷️ Source System Linkage">
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={sourceLink} layout="vertical" margin={{left:20}}><XAxis type="number" tick={{fill:"#64748B",fontSize:9}}/><YAxis type="category" dataKey="name" tick={{fill:"#64748B",fontSize:9}} width={110}/><Tooltip contentStyle={ttStyle}/>
            <Bar dataKey="value" name="Customers" radius={[0,4,4,0]}>{sourceLink.map((e,i)=><Cell key={i} fill={PAL[i]}/>)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
    <Card title="📋 Expanded Star Schema — 11 Tables">
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:8}}>
        {[{n:"dim_customer",t:"Dimension SCD2",r:"500",c:C.green,f:["customer_uid (PK)","full_name, email","segment, status","lifetime_value"]},
          {n:"dim_product",t:"Dimension",r:"80",c:C.gold,f:["product_id (PK)","category, subcategory","unit_price, margin","is_recurring"]},
          {n:"dim_customer_lifecycle",t:"Dimension",r:"500",c:C.purple,f:["customer_uid (FK)","lifecycle_stage","churn_risk_score","cohort, tenure"]},
          {n:"dim_date",t:"Dimension",r:"762",c:C.cyan,f:["date_key (PK)","year, quarter, month","day_of_week"]},
          {n:"fact_sales",t:"Fact",r:"3,500",c:C.accent,f:["order_id (PK)","customer_uid → dim","product_id → dim","line_total, profit"]},
          {n:"fact_interactions",t:"Fact",r:"6,000",c:C.blue,f:["interaction_id (PK)","customer_uid → dim","channel, sentiment","csat_score"]},
          {n:"fact_clickstream",t:"Fact",r:"25,000",c:C.teal,f:["event_id (PK)","session_id, page_url","event_type, device","referrer, is_converted"]},
          {n:"fact_pipeline",t:"Fact",r:"1,200",c:C.pink,f:["deal_id (PK)","customer_uid → dim","stage, lead_source","deal_amount, is_won"]},
          {n:"fact_realtime_metrics",t:"Fact (Time-Series)",r:"168",c:C.lime,f:["timestamp (PK)","active_users, page_views","api_calls, latency","dq_pass_rate"]},
          {n:"fact_fraud_signals",t:"Fact",r:"450",c:C.red,f:["alert_id (PK)","fraud_type, severity","risk_score, status","financial_impact"]},
          {n:"mdm_match_pairs",t:"Audit",r:"200",c:"#6B7280",f:["pair_id (PK)","customer_a, customer_b","match_score, tier","name/email/phone sim"]},
        ].map((t,i)=>(
          <div key={i} style={{background:C.card2,borderRadius:6,padding:10,borderTop:`3px solid ${t.c}`,fontSize:10}}>
            <div style={{fontWeight:700,color:t.c,fontSize:11,marginBottom:2}}>{t.n}</div>
            <div style={{color:C.muted,fontSize:9,marginBottom:6}}>{t.t} • {t.r} rows</div>
            {t.f.map((f,fi)=><div key={fi} style={{padding:"1px 0",borderBottom:`1px solid ${C.border}22`,fontFamily:"monospace",fontSize:9,color:C.text}}>{f}</div>)}
          </div>
        ))}
      </div>
    </Card>
  </div>);
}

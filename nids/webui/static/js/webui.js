
function getSelectedDeviceRole(id, role) {
    var ret = document.createElement('select');
    ret.classList.add("form-control");
    ret.id = "drole-" + id;
    var brg = document.createElement('option');
    brg.value = "bridge";
    brg.innerHTML = "Bridge";
    brg.selected = (role == "bridge");
    ret.add(brg);
    var fld = document.createElement('option');
    fld.value = "field";
    fld.innerHTML = "Field network";
    fld.selected = (role == "field");
    ret.add(fld);
    var hnp = document.createElement('option');
    hnp.value = "honeypot";
    hnp.innerHTML = "Honeypot network";
    hnp.selected = (role == "honeypot");
    ret.add(hnp);
    var spn = document.createElement('option');
    spn.value = "span";
    spn.innerHTML = "Traffic mirror";
    spn.selected = (role == "span");
    ret.add(spn);
    var una = document.createElement('option');
    una.value = "na";
    una.innerHTML = "Unassigned";
    una.selected = (role == "na");
    ret.add(una);
    return ret;
}

function getSelectedHostRole(id, role) {
    var ret = document.createElement('select');
    ret.classList.add('form-control');
    ret.id = "hrole-" + id;
    var act = document.createElement('option');
    act.value = "actuator";
    act.innerHTML = "Actuator";
    act.selected = (role == "actuator");
    ret.add(act);
    var hmi = document.createElement('option');
    hmi.value = "hmi";
    hmi.innerHTML = "HMI";
    hmi.selected = (role == "hmi");
    ret.add(hmi);
    var plc = document.createElement('option');
    plc.value = "plc";
    plc.innerHTML = "PLC";
    plc.selected = (role == "plc");
    ret.add(plc);
    var sensor = document.createElement('option');
    sensor.value = "sensor";
    sensor.innerHTML = "Sensor";
    sensor.selected = (role == "sensor");
    ret.add(sensor);
    var una = document.createElement('option');
    una.value = "na";
    una.innerHTML = "Unassigned";
    una.selected = (role == "na");
    ret.add(una);
    return ret;
}

function getActiveApps() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var appid = document.getElementById('flowappid');
            var appids = JSON.parse(this.responseText);
            appids = appids['appids'];
            if (appid.options.length != appids.length) {
                for (i = 0; i < appids.length; i ++) {
                    var value = appids[i];
                    var opt = document.createElement('option');
                    opt.value = value;
                    opt.innerHTML = value;
                    if (value == "org.onosproject.fwd")
                        opt.selected = true;
                    appid.add(opt);
                };
            }
        }
    }
    xhttp.open('GET', '/getappids', true);
    xhttp.send();
}

function refreshDevices() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var tbldata = JSON.parse(this.responseText);
            var tblcontent = "";
            var tblelem = document.getElementById('devices');
            while(tblelem.rows.length > 0)
                tblelem.deleteRow(0);
            for (d in tbldata.devs) {
                tblelem.insertRow();
                var lrow = tblelem.lastElementChild;
                currdev = tbldata.devs[d];
                annot = currdev.annotations;
                lrow.insertCell();
                var ccell = lrow.lastElementChild;
                ccell.innerHTML = currdev.id;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                if (currdev.available) 
                    ccell.innerHTML = "YES";
                else
                    ccell.innerHTML = "NO";
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = currdev.humanReadableLastUpdate;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = currdev.mfr;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = currdev.hw;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = annot.protocol;
                var ig = document.createElement('div');
                ig.classList.add("input-group");
                ig.classList.add("input-group-sm");
                ig.appendChild(getSelectedDeviceRole(currdev.id, currdev.role));
                var selrole = ig.lastElementChild;
                iga = document.createElement('div');
                iga.classList.add("input-group-append");
                var btn = document.createElement('button');
                btn.type = "button";
                btn.classList.add("btn");
                btn.classList.add("btn-sm");
                btn.classList.add("btn-outline-success");
                btn.onclick = (function (did, rvl) { return function(){ updateDeviceRole(did, rvl); }; })(currdev.id, selrole.value);
                btn.innerHTML = "Update";
                iga.appendChild(btn);
                ig.appendChild(iga);
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.appendChild(ig);
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = ((currdev.spanport == 0) ? "Local" : ((currdev.spanport > 0) ? currdev.spanport : "No mirror"));
            }
        }
    }
    xhttp.open('GET', '/getdevices', true);
    xhttp.send();
}

function refreshHosts() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            tbldata = JSON.parse(this.responseText);
            tblelem = document.getElementById('hosts');
            while(tblelem.rows.length > 0)
                tblelem.deleteRow(0);
            for (h in tbldata.hosts) {
                currhost = tbldata.hosts[h];
                tblelem.insertRow();
                var lrow = tblelem.lastElementChild;
                lrow.insertCell();
                var ccell = lrow.lastElementChild;
                ccell.innerHTML = currhost.mac;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = currhost.ipAddresses.join(', ');
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                var ig = document.createElement('div');
                ig.classList.add('input-group');
                ig.classList.add('input-group-sm');
                var hname = document.createElement('input');
                hname.classList.add('form-control');
                hname.id = "hname-" + h;
                hname.type = "text";
                hname.value = currhost.name;
                ig.appendChild(hname);
                var iga = document.createElement('div');
                iga.classList.add('input-group-append');
                var btn = document.createElement('button');
                btn.classList.add('btn');
                btn.classList.add('btn-sm');
                btn.classList.add('btn-outline-success');
                btn.onclick = (function(ip, nm){ return function() { updateHostName(ip, nm); }; })(currhost.ipAddresses[0], hname.id);
                btn.innerHTML = "Update";
                iga.appendChild(btn);
                ig.appendChild(iga);
                ccell.appendChild(ig);
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                for (l in currhost.locations) {
                    var cloc = currhost.locations[l];
                    cloc = cloc.elementId + " port: " + cloc.port + ",";
                    cloc = cloc.substr(0, cloc.length - 1);
                    ccell.innerHTML += cloc;
                }
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ig = document.createElement('div');
                ig.classList.add('input-group');
                ig.classList.add('input-group-sm');
                var currhrole = getSelectedHostRole(h, currhost.role);
                ig.appendChild(currhrole);
                iga = document.createElement('div');
                iga.classList.add('input-group-append');
                btn = document.createElement('button');
                btn.classList.add('btn');
                btn.classList.add('btn-sm');
                btn.classList.add('btn-outline-success');
                btn.onclick = (function(m, r){ return function() { updateHostRole(m, r); }; })(currhost.mac.split(" ")[0], currhrole.value);
                btn.innerHTML = "Update";
                iga.appendChild(btn);
                ig.appendChild(iga);
                ccell.appendChild(ig);
            }
        }
    }
    xhttp.open('GET', '/gethosts', true);
    xhttp.send();
}

function refreshTopSniffed() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            tbldata = JSON.parse(this.responseText);
            tbldata = tbldata.top;
            tblelem = document.getElementById('topsniffed');
            accum = 0;
            cnt = 1;
            var lrow;
            var ccell;
            while(tblelem.rows.length > 0)
                tblelem.deleteRow(0);
            for(datap in tbldata) {
                srdt = datap.split('/');
                tblelem.insertRow();
                lrow = tblelem.lastElementChild;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = cnt;
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = srdt[0];
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = srdt[1];
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = srdt[2];
                lrow.insertCell();
                ccell = lrow.lastElementChild;
                ccell.innerHTML = tbldata[datap];
                accum += tbldata[datap];
                cnt += 1;
            }
            tblelem.insertRow();
            lrow = tblelem.lastElementChild;
            lrow.classList.add('table-secondary');
            lrow.classList.add('font-weight-bold');
            lrow.insertCell();
            lrow.insertCell();
            ccell = lrow.lastElementChild;
            ccell.colSpan = 3;
            ccell.innerHTML = "Total";
            lrow.insertCell();
            ccell = lrow.lastElementChild;
            ccell.innerHTML = accum;
        }
    }
    xhttp.open('GET', '/gettopsniffed', true);
    xhttp.send();
}

function refreshPPSChart() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            rawdata = JSON.parse(this.responseText);
            rawdata = rawdata.pps;
            var ppsdata = new Array(rawdata.length);
            var enipdata = new Array(rawdata.length);
            var dt = 0;
            var maxv = 0;
            while (dt < rawdata.length) {
                dpt = rawdata[dt];
                currt = new Date(Math.round(dpt[0]*1000));
                ppsdata[dt] = { t: currt, y: dpt[1] };
                enipdata[dt] = { t: currt, y: dpt[2] };
                maxv = (dpt[1] > maxv) ? dpt[1] : maxv;
                maxv = (dpt[2] > maxv) ? dpt[2] : maxv;
                dt ++;
            }
            var ctcol = document.getElementById('chpps');
            if(ctcol.hasChildNodes())
                ctcol.removeChild(ctcol.lastElementChild);
            var ctx = document.createElement('canvas');
            ctx.classList.add('h-100');
            ctcol.appendChild(ctx);
            ctx = ctx.getContext("2d");
            var ppschart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: 'Sniffed IP packets',
                            data: ppsdata,
                            borderColor: 'rgba(199,91,18,1.0)',
                            backgroundColor: 'rgba(199,91,18,0.33)',
                            pointRadius: 0,
                        },
                        {
                            label: 'Sniffed ENIP packets',
                            data: enipdata,
                            borderColor: 'rgba(0,133,66,1.0)',
                            backgroundColor: 'rgba(0,133,66,0.33)',
                            pointRadius: 0,
                        }
                    ]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            distribution: 'linear',
                            position: 'bottom'
                        }],
                        yAxes: [{
                            type: 'linear',
                            ticks: {
                                beginAtZero: true,
                                suggestedMax: (maxv > 10) ? Math.round(maxv * 1.15) : ((maxv > 0) ? maxv * 1.15 : 1),
                            },
                            stacked: false,
                        }]
                    },
                    animation: {
                        duration: 0,
                    },
                    elements: {
                        line: {
                            tension: 0.2,
                            borderWidth: 2,
                        },
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        position: 'top',
                        text: 'Last 10 minutes',
                        fontColor: '#008542',
                        fontSize: 16,
                    },
                    responsive: true,
                }
            });
        }
    }
    xhttp.open('GET', '/getppsdata', true);
    xhttp.send();
    refreshTopSniffed();
}

function refreshGroups() {
    var devs = document.getElementById("devices");
    var gdev = document.getElementById('group-device');
    if(devs) {
        if (gdev.length != devs.rows.length) {
            while(gdev.options.length > 0)
                gdev.options.remove(0);
            for (i = 0; i < devs.rows.length; i++) {
                var devid = devs.rows[i].cells[0].innerHTML;
                var opt = document.createElement('option');
                opt.value = devid;
                opt.innerHTML = devid;
                gdev.add(opt);
            }
        }
        if (gdev.selectedIndex >= 0) {
            var devid = gdev.options[gdev.selectedIndex].value;
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    grdata = JSON.parse(this.responseText);
                    grdata = grdata.groups;
                    tblelem = document.getElementById('device-groups');
                    while(tblelem.rows.length > 0)
                        tblelem.deleteRow(0);
                    for (g in grdata) {
                        gr = grdata[g];
                        gid = gr.id;
                        acook = gr.appCookie;
                        bck = gr.buckets;
                        tblelem.insertRow();
                        var lrow = tblelem.lastElementChild;
                        lrow.insertCell();
                        var ccell = lrow.lastElementChild;
                        ccell.innerHTML = gid;
                        ccell.rowSpan = bck.length;
                        ccell.style.verticalAlign = 'middle';
                        ccell.style.textAlign = "center";
                        lrow.insertCell();
                        ccell = lrow.lastElementChild;
                        ccell.innerHTML = acook;
                        ccell.rowSpan = bck.length;
                        ccell.style.verticalAlign = 'middle';
                        ccell.style.textAlign = "center";
                        for(b in bck) {
                            bkt = bck[b];
                            if (b > 0) {
                                tblelem.insertRow();
                                lrow = tblelem.lastElementChild;
                            }
                            lrow.insertCell();
                            ccell = lrow.lastElementChild;
                            ccell.innerHTML = bkt.bucketId;
                            ccell.style.textAlign = "center";
                            lrow.insertCell();
                            ccell = lrow.lastElementChild;
                            ccell.innerHTML = "";
                            ccell.style.textAlign = "center";
                            bact = bkt.treatment;
                            bact = bact.instructions;
                            for (i in bact) {
                                cact = bact[i];
                                for(el in cact) {
                                    ccell.innerHTML += el + "=" + cact[el] + " ";
                                }
                                ccell.innerHTML += "<br>";
                            }
                            if (b == 0) {
                                lrow.insertCell();
                                ccell = lrow.lastElementChild;
                                var delbtn = document.createElement('button');
                                delbtn.type = "button";
                                delbtn.classList.add('btn');
                                delbtn.classList.add('btn-sm');
                                delbtn.classList.add('btn-danger');
                                delbtn.onclick = (function (did, ack){ return function() { deleteGroup(did, ack); }; })(devid, acook);
                                delbtn.innerHTML = "delete";
                                ccell.rowSpan = bck.length;
                                ccell.style.verticalAlign = 'middle';
                                ccell.style.textAlign = "center";
                                ccell.appendChild(delbtn);
                            }
                        }

                    }
                }
            }
            xhttp.open('POST', '/getdevicegroups', true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("devid=" + devid);
        }
    }
}

function extractCriteria(criteria) {
    var out = criteria['type'];
    switch(out) {
        case 'ETH_TYPE':
            out += ': ' + criteria['ethType'];
            break;
        case 'ETH_DST':
        case 'ETH_SRC':
        case 'IPV6_ND_SLL':
        case 'IPV6_ND_TLL':
            out += ': ' + criteria['mac'];
            break;
        case 'IN_PORT':
        case 'IN_PHY_PORT':
            out += ': ' + criteria['port'];
            break;
        case 'METADATA':
            out += ': ' + criteria['metadata'];
            break;
        case 'VLAN_VID':
            out += ': ' + criteria['vlanId'];
            break;
        case 'VLAN_PCP':
            out += ': ' + criteria['priority'];
            break;
        case 'INNER_VLAN_VID':
            out += ': ' + criteria['innerVlanId'];
            break;
        case 'INNER_VLAN_PCP':
            out += ': ' + criteria['innerPriority'];
            break;
        case 'IP_DSCP':
            out += ': ' + criteria['ipDscp'];
            break;
        case 'IP_ECN':
            out += ': ' + criteria['ipEcn'];
            break;
        case 'IP_PROTO':
            out += ': ' + criteria['protocol'];
            break;
        case 'IPV4_SRC':
        case 'IPV4_DST':
        case 'IPV6_SRC':
        case 'IPV6_DST':
            out += ': ' + criteria['ip'];
            break;
        case 'TCP_SRC':
        case 'TCP_DST':
            out += ': ' + criteria['tcpPort'];
            break;
        case 'UDP_SRC':
        case 'UDP_DST':
            out += ': ' + criteria['udpPort'];
            break;
        case 'SCTP_SRC':
        case 'SCTP_DST':
            out += ': ' + criteria['sctpPort'];
            break;
        case 'ICMPV4_TYPE':
            out += ': ' + criteria['icmpType'];
            break;
        case 'ICMPV4_CODE':
            out += ': ' + criteria['icmpCode'];
            break;
        case 'IPV6_FLABEL':
            out += ': ' + criteria['flowlabel'];
            break;
        case 'ICMPV6_TYPE':
            out += ': ' + criteria['icmpv6Type'];
            break;
        case 'ICMPV6_CODE':
            out += ': ' + criteria['icmpv6Code'];
            break;
        case 'IPV6_ND_TARGET':
            out += ': ' + criteria['targetAddress'];
            break;
        case 'MPLS_LABEL':
            out += ': ' + criteria['label'];
            break;
        case 'IPV6_EXTHDR':
            out += ': ' + criteria['exthdrFlags'];
            break;
        case 'OCH_SIGID':
            out += ': ' + criteria['ochSignalId'];
            break;
        case 'GRID_TYPE':
            out += ': ' + criteria['gridType'];
            break;
        case 'CHANNEL_SPACING':
            out += ': ' + criteria['channelSpacing'];
            break;
        case 'SPACING_MULTIPLIER':
            out += ': ' + criteria['spacingMultiplier'];
            break;
        case 'SLOT_GRANULARITY':
            out += ': ' + criteria['slotGranularity'];
            break;
        case 'OCH_SIGTYPE':
            out += ': ' + criteria['ochSignalType'];
            break;
        case 'TUNNEL_ID':
            out += ': ' + criteria['tunnelId'];
            break;
        case 'ODU_SIGID':
            out += ': ' + criteria['oduSignalId'];
            break;
        case 'ODU_SIGTYPE':
            out += ': ' + criteria['oduSignalType'];
            break;
    }
    return out;
}

function extractTreatment(treatment) {
    var out = "";
    for (i = 0; i < treatment.length; i++) {
        out += treatment[i]['type'];
        switch(out) {
            case 'OUTPUT':
                out += ': ' + treatment[i]['port'];
                break;
            case 'TABLE':
                out += ': ' + treatment[i]['tableId'];
                break;
            case 'GROUP':
                out += ': ' + treatment[i]['groupId'];
                break;
            case 'METER':
                out += ': ' + treatment[i]['meterId'];
                break;
            case 'QUEUE':
                out += ': id=' + treatment[i]['queueId'] + ' port=' + treatment[i]['port'];
                break;
            case 'L0MODIFICATION':
            case 'L1MODIFICATION':
            case 'L2MODIFICATION':
            case 'L3MODIFICATION':
            case 'L4MODIFICATION':
                out += ': subtype=' + treatment[i]['subtype'];
                break;
            case 'NOACTION':
                break;
            default:
                out += ': unknown'
        }
        out += "<br>";
    }
    return out;
}

function refreshFlows() {
    var devs = document.getElementById("devices");
    if(devs) {
        var fdev = document.getElementById('flows-device');
        if (fdev.length != devs.rows.length) {
            while (fdev.options.length > 0)
                fdev.options.remove(0);
            for (i = 0; i < devs.rows.length; i++) {
                var devid = devs.rows[i].cells[0].innerHTML;
                var opt = document.createElement('option');
                opt.value = devid;
                opt.innerHTML = devid;
                fdev.add(opt);
            }
        }
        if (fdev.selectedIndex >= 0) {
            var devid = fdev.options[fdev.selectedIndex].value;
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var flows = JSON.parse(this.responseText);
                    flows = flows.flows;
                    var tbdy = document.getElementById('device-flows');
                    while (tbdy.rows.length > 0)
                        tbdy.deleteRow(0);
                    for (f in flows) {
                        var flow = flows[f];
                        tbdy.insertRow();
                        var crow = tbdy.lastElementChild;
                        crow.insertCell();
                        var ccell = crow.lastElementChild;
                        ccell.innerHTML = flow['id'];
                        crow.insertCell();
                        ccell = crow.lastElementChild;
                        ccell.innerHTML = flow['state'];
                        crow.insertCell();
                        ccell = crow.lastElementChild;
                        ccell.innerHTML = flow['priority'];
                        crow.insertCell();
                        ccell = crow.lastElementChild;
                        var tdt = flow['selector'];
                        tdt = tdt['criteria'];
                        for(i in tdt)
                            ccell.innerHTML += extractCriteria(tdt[i]) + '<br>';
                        crow.insertCell();
                        ccell = crow.lastElementChild;
                        tdt = flow['treatment'];
                        ccell.innerHTML = extractTreatment(tdt['instructions']);
                        ccell.innerHTML += ' cleared:' + ((tdt['clearDeferred']) ? 'true' : 'false');
                        crow.insertCell();
                        ccell = crow.lastElementChild;
                        ccell.innerHTML = flow['appId'];
                        crow.insertCell();
                        ccell = crow.lastElementChild;
                        var btn = document.createElement('button');
                        btn.classList.add('btn');
                        btn.classList.add('btn-sm');
                        btn.classList.add('btn-danger');
                        btn.onclick = (function (did, fid){ return function() { deleteFlow(did, fid); }; })(devid, flow['id']);
                        btn.innerHTML = "delete";
                        ccell.appendChild(btn);
                    }
                }
            }
            xhttp.open('POST', '/getdeviceflows', true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("devid=" + devid);
        }
    }
    getActiveApps();
}

function refreshAll() {
    localTime = document.getElementById('localtime');
    ctime = new Date();
    localTime.innerHTML = ctime.toLocaleDateString() + " " + ctime.toLocaleTimeString();
    refreshDevices();
    refreshHosts();
    refreshPPSChart();
    refreshGroups();
    refreshFlows();
}

function addAction() {
    var atype = document.getElementById('actiontype').value;
    var stype = document.getElementById('actionsubtype').value;
    var avalue = document.getElementById('actionvalue').value;
    document.getElementById('actionvalue').value = null;
    if(avalue.length > 0) {
        if(stype == "NA") {
            switch(atype) {
                case "OUTPUT":
                    avalue = "port=" + avalue;
                    break;
                case "TABLE":
                    avalue = "tableId=" + avalue;
                    break;
                case "METER":
                    avalue = "meterId=" + avalue;
                    break;
                default:
                    avalue = "value=" + avalue;
            }
        }
        else {
            switch(stype) {
                case "VLAN_ID":
                    avalue = "vlanId=" + avalue;
                    break;
                case "VLAN_PCP":
                    avalue = "vlanPcp=" + avalue;
                    break;
                case "ETH_SRC":
                case "ETH_DST":
                    avalue = "mac=" + avalue;
                    break;
                case "MPLS_LABEL":
                    avalue = "label=" + avalue;
                    break;
                case "MPLS_PUSH":
                    avalue = "ethernetType=" + avalue;
                    break;
                case "TUNNEL_ID":
                    avalue = "tunnelId=" + avalue;
                    break;
                case "IPV4_SRC":
                case "IPV4_DST":
                case "IPV6_SRC":
                case "IPV6_DST":
                    avalue = "ip=" + avalue;
                    break;
                case "IPV6_FLABEL":
                    avalue = "flowLabel=" + avalue;
                    break;
                case "TCP_SRC":
                    avalue = "tcpPort=" + avalue;
                    break;
                case "UDP_SRC":
                    avalue = "udpPort=" + avalue;
                    break;
                default:
                    avalue = "value=" + avalue;
            }
        }
        var abody = document.getElementById('bucketactions');
        abody.insertRow();
        var arows = abody.rows;
        var crow = arows.item(arows.length - 1);
        crow.insertCell();
        crow.insertCell();
        crow.insertCell();
        crow.cells[0].innerHTML = atype;
        crow.cells[1].innerHTML = stype;
        crow.cells[2].innerHTML = avalue;
    }
    else {
        alert('Missing action value.')
    }
}

function removeAction() {
    var bbody = document.getElementById('bucketactions');
    if (bbody.rows.length > 0)
        bbody.deleteRow(bbody.rows.length - 1);
}

function addBucket() {
    var actions = document.getElementById('bucketactions');
    var bucket = [];
    while(actions.rows.length > 0) {
        var crow = actions.rows[0].cells;
        var cact = {};
        cact.type = crow[0].innerHTML;
        if(crow[1].innerHTML != "NA")
            cact.subtype = crow[1].innerHTML;
        var cval = crow[2].innerHTML.split("=");
        cact[cval[0]] = cval[1];
        bucket.push(cact);
        actions.deleteRow(0);
    }
    var confirmed = (bucket.length > 0) ? true : confirm('You are about to add a bucket with no actions.\n\nIs this OK?');
    if (confirmed) {
        var grpb = document.getElementById('groupbuckets').innerHTML;
        if(grpb.length == 0)
            grpb = JSON.stringify(bucket);
        else
            grpb = grpb.concat("\n", JSON.stringify(bucket));
        document.getElementById('groupbuckets').innerHTML = grpb;
    }
}

function removeBucket() {
    var grpb = document.getElementById('groupbuckets').innerHTML;
    grpb = grpb.substring(0,grpb.lastIndexOf("\n"));
    document.getElementById('groupbuckets').innerHTML = grpb;
}

function updateHostName(ip, name) {
    hname = document.getElementById(name).value;
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/updatehostname', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("ip=" + ip + "&name=" + hname);
    refreshHosts();
}

function updateDeviceRole(id, role) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/updatedevrole', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("id=" + id + "&role=" + role);
    refreshDevices();
}

function updateHostRole(mac, role) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/updatehostrole', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("mac=" + mac + "&role=" + role);
    refreshHosts();
}

function updateActionSubtype() {
    atype = document.getElementById('actiontype').selectedOptions[0].value;
    stype = document.getElementById('actionsubtype');
    while(stype.options.length > 0)
        stype.options.remove(0);
    switch(atype) {
        case "L2MODIFICATION":
            opt = document.createElement('option');
            opt.value = "VLAN_ID";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "VLAN_PCP";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "ETH_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "ETH_DST";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "MPLS_LABEL";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "MPLS_PUSH";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "TUNNEL_ID";
            opt.innerHTML = opt.value;
            stype.add(opt);
            break;
        case "L3MODIFICATION":
            opt = document.createElement('option');
            opt.value = "IPV4_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV4_DST";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV6_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV6_DST";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV6_FLABEL";
            opt.innerHTML = opt.value;
            stype.add(opt);
            break;
        case "L4MODIFICATION":
            opt = document.createElement('option');
            opt.value = "TCP_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "UDP_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            break;
        default:
            opt = document.createElement('option');
            opt.value = "NA";
            opt.innerHTML = "N/A";
            opt.selected = true;
            stype.add(opt);
    }
    updateActionLabel();
}

function updateActionLabel() {
    lbl = document.getElementById('actionvallbl');
    aval = document.getElementById('actionvalue');
    atype = document.getElementById('actiontype').selectedOptions[0].value;
    stype = document.getElementById('actionsubtype').selectedOptions[0].value;
    if(stype == 'NA') {
        switch(atype) {
            case "OUTPUT":
                lbl.innerHTML = "Port";
                aval.placeholder = "123";
                aval.pattern = "^[1-9][0-9]*$";
                break;
            case "TABLE":
                lbl.innerHTML = "Table ID";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "METER":
                lbl.innerHTML = "Meter ID";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            default:
                lbl.innerHTML = "Value";
                aval.placeholder = "value";
                aval.pattern = "value";
        }
    }
    else {
        switch(stype) {
            case "VLAN_ID":
                lbl.innerHTML = "vlanId";
                aval.placeholder = "1-4094";
                aval.pattern = "^(?:40(?:[0-8][0-9]|9[0-4])|[1-3][0-9]{3}|[1-9][0-9]{1,2}|[1-9])$";
                break;
            case "VLAN_PCP":
                lbl.innerHTML = "vlanPcp";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "ETH_SRC":
            case "ETH_DST":
                lbl.innerHTML = "mac";
                aval.placeholder = "12:34:56:ab:cd:ef";
                aval.pattern = "^[0-9a-fA-F]{2}(?:[:][0-9a-fA-F]{2}){5}$";
                break;
            case "MPLS_LABEL":
                lbl.innerHTML = "label";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "MPLS_PUSH":
                lbl.innerHTML = "ethernetType";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "TUNNEL_ID":
                lbl.innerHTML = "tunnelId";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "IPV4_SRC":
            case "IPV4_DST":
                lbl.innerHTML = "ip";
                aval.placeholder = "1.2.3.4";
                aval.pattern = "^(?:(?:2(?:[1-4]\\d|5[0-5])|1\\d{2}|[1-9]?\\d)[.]){3}(?:2(?:[1-4]\\d|5[0-5])|1\\d{2}|[1-9]?\\d)$";
                break;
            case "IPV6_SRC":
            case "IPV6_DST":
                lbl.innerHTML = "ip";
                aval.placeholder = "1234::abcd";
                aval.pattern = "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$";
                break;
            case "IPV6_FLABEL":
                lbl.innerHTML = "flowLabel";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "TCP_SRC":
                lbl.innerHTML = "tcpPort";
                aval.placeholder = "1-65535";
                aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
                break;
            case "UDP_SRC":
                lbl.innerHTML = "udpPort";
                aval.placeholder = "1-65535";
                aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
                break;
            default:
                lbl.innerHTML = "Value";
                aval.placeholder = "value";
                aval.pattern = "value";
        }
    }
}

function updateInstructionSubtype() {
    atype = document.getElementById('instrtype').selectedOptions[0].value;
    stype = document.getElementById('instrsubtype');
    while(stype.options.length > 0)
        stype.options.remove(0);
    switch(atype) {
        case "L2MODIFICATION":
            opt = document.createElement('option');
            opt.value = "VLAN_ID";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "VLAN_PCP";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "ETH_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "ETH_DST";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "MPLS_LABEL";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "MPLS_PUSH";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "TUNNEL_ID";
            opt.innerHTML = opt.value;
            stype.add(opt);
            break;
        case "L3MODIFICATION":
            opt = document.createElement('option');
            opt.value = "IPV4_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV4_DST";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV6_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV6_DST";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "IPV6_FLABEL";
            opt.innerHTML = opt.value;
            stype.add(opt);
            break;
        case "L4MODIFICATION":
            opt = document.createElement('option');
            opt.value = "TCP_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            opt = document.createElement('option');
            opt.value = "UDP_SRC";
            opt.innerHTML = opt.value;
            stype.add(opt);
            break;
        default:
            opt = document.createElement('option');
            opt.value = "NA";
            opt.innerHTML = "N/A";
            opt.selected = true;
            stype.add(opt);
    }
    updateInstructionLabel();
}

function updateInstructionLabel() {
    lbl = document.getElementById('instrvallbl');
    aval = document.getElementById('instrvalue');
    aval.disabled = false;
    atype = document.getElementById('instrtype').selectedOptions[0].value;
    stype = document.getElementById('instrsubtype').selectedOptions[0].value;
    if(stype == 'NA') {
        switch(atype) {
            case "OUTPUT":
                lbl.innerHTML = "Port";
                aval.placeholder = "123";
                aval.pattern = "^[1-9][0-9]*$";
                break;
            case "GROUP":
                lbl.innerHTML = "Group ID";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "TABLE":
                lbl.innerHTML = "Table ID";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "METER":
                lbl.innerHTML = "Meter ID";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "NOACTION":
                lbl.innerHTML = "N/A";
                aval.placeholder = "N/A";
                aval.disabled = true;
                break;
            default:
                lbl.innerHTML = "Value";
                aval.placeholder = "value";
                aval.pattern = "value";
        }
    }
    else {
        switch(stype) {
            case "VLAN_ID":
                lbl.innerHTML = "vlanId";
                aval.placeholder = "1-4094";
                aval.pattern = "^(?:40(?:[0-8][0-9]|9[0-4])|[1-3][0-9]{3}|[1-9][0-9]{1,2}|[1-9])$";
                break;
            case "VLAN_PCP":
                lbl.innerHTML = "vlanPcp";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "ETH_SRC":
            case "ETH_DST":
                lbl.innerHTML = "mac";
                aval.placeholder = "12:34:56:ab:cd:ef";
                aval.pattern = "^[0-9a-fA-F]{2}(?:[:][0-9a-fA-F]{2}){5}$";
                break;
            case "MPLS_LABEL":
                lbl.innerHTML = "label";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "MPLS_PUSH":
                lbl.innerHTML = "ethernetType";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "TUNNEL_ID":
                lbl.innerHTML = "tunnelId";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "IPV4_SRC":
            case "IPV4_DST":
                lbl.innerHTML = "ip";
                aval.placeholder = "1.2.3.4";
                aval.pattern = "^(?:(?:2(?:[1-4]\\d|5[0-5])|1\\d{2}|[1-9]?\\d)[.]){3}(?:2(?:[1-4]\\d|5[0-5])|1\\d{2}|[1-9]?\\d)$";
                break;
            case "IPV6_SRC":
            case "IPV6_DST":
                lbl.innerHTML = "ip";
                aval.placeholder = "1234::abcd";
                aval.pattern = "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$";
                break;
            case "IPV6_FLABEL":
                lbl.innerHTML = "flowLabel";
                aval.placeholder = "123";
                aval.pattern = "[0-9]+";
                break;
            case "TCP_SRC":
                lbl.innerHTML = "tcpPort";
                aval.placeholder = "1-65535";
                aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
                break;
            case "UDP_SRC":
                lbl.innerHTML = "udpPort";
                aval.placeholder = "1-65535";
                aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
                break;
            default:
                lbl.innerHTML = "Value";
                aval.placeholder = "value";
                aval.pattern = "value";
        }
    }
}

function addInstruction() {
    var atype = document.getElementById('instrtype').value;
    var stype = document.getElementById('instrsubtype').value;
    var avalue = document.getElementById('instrvalue').value;
    document.getElementById('instrvalue').value = null;
    if(avalue.length > 0 || atype == "NOACTION") {
        if(stype == "NA") {
            switch(atype) {
                case "OUTPUT":
                    avalue = "port=" + avalue;
                    break;
                case "GROUP":
                    avalue = "groupId=" + avalue;
                    break;
                case "TABLE":
                    avalue = "tableId=" + avalue;
                    break;
                case "METER":
                    avalue = "meterId=" + avalue;
                    break;
                case "NOACTION":
                    avalue = "NA";
                    break;
                default:
                    avalue = "value=" + avalue;
            }
        }
        else {
            switch(stype) {
                case "VLAN_ID":
                    avalue = "vlanId=" + avalue;
                    break;
                case "VLAN_PCP":
                    avalue = "vlanPcp=" + avalue;
                    break;
                case "ETH_SRC":
                case "ETH_DST":
                    avalue = "mac=" + avalue;
                    break;
                case "MPLS_LABEL":
                    avalue = "label=" + avalue;
                    break;
                case "MPLS_PUSH":
                    avalue = "ethernetType=" + avalue;
                    break;
                case "TUNNEL_ID":
                    avalue = "tunnelId=" + avalue;
                    break;
                case "IPV4_SRC":
                case "IPV4_DST":
                case "IPV6_SRC":
                case "IPV6_DST":
                    avalue = "ip=" + avalue;
                    break;
                case "IPV6_FLABEL":
                    avalue = "flowLabel=" + avalue;
                    break;
                case "TCP_SRC":
                    avalue = "tcpPort=" + avalue;
                    break;
                case "UDP_SRC":
                    avalue = "udpPort=" + avalue;
                    break;
                default:
                    avalue = "value=" + avalue;
            }
        }
        var abody = document.getElementById('flowinstructions');
        abody.insertRow();
        var arows = abody.rows;
        var crow = arows.item(arows.length - 1);
        crow.insertCell();
        crow.insertCell();
        crow.insertCell();
        crow.cells[0].innerHTML = atype;
        crow.cells[1].innerHTML = stype;
        crow.cells[2].innerHTML = avalue;
    }
    else {
        alert('Missing instruction value.')
    }
}

function removeInstruction() {
    var bbody = document.getElementById('flowinstructions');
    if (bbody.rows.length > 0)
        bbody.deleteRow(bbody.rows.length - 1);
}

function createGroup() {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/creategroup', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var pdata = "";
    pdata += "devid=" + document.getElementById('group-device').value;
    pdata += "&grpid=" + document.getElementById('newgroupid').value;
    pdata += "&appck=" + document.getElementById('newgroupappck').value;
    var bck = document.getElementById('groupbuckets').innerHTML.split("\n");
    var buckets = [];
    for (i = 0; i < bck.length; i ++) {
        var nbck = JSON.parse(bck[i]);
        buckets.push(nbck);
    }
    pdata += "&buckets=" + btoa(JSON.stringify(buckets));
    xhttp.send(pdata);
    document.getElementById('groupbuckets').innerHTML = '';
    document.getElementById('newgroupid').value = '';
    document.getElementById('newgroupappck').value = '';
    refreshGroups();
}

function deleteGroup(devid, appck) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/deletegroup', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var pdata = "";
    pdata += "devid=" + devid;
    pdata += "&appck=" + appck;
    xhttp.send(pdata);
    refreshGroups();
}

function updateCriteriaLabel() {
    lbl = document.getElementById('flowcritlbl');
    aval = document.getElementById('flowcritval');
    atype = document.getElementById('flowcrittype').selectedOptions[0].value;
    switch(atype) {
        case "ETH_DST":
        case "ETH_SRC":
        case "IPV6_ND_SLL":
        case "IPV6_ND_TLL":
            lbl.innerHTML = "mac";
            aval.placeholder = "12:34:56:ab:cd:ef";
            aval.pattern = "^[0-9a-fA-F]{2}(?:[:][0-9a-fA-F]{2}){5}$";
            break;
        case "ETH_TYPE":
            lbl.innerHTML = "ethType";
            aval.placeholder = "0x12ab";
            aval.pattern = "^0x[0-9a-fA-F]{4}$";
            break;
        case "IN_PORT":
        case "IN_PHY_PORT":
            lbl.innerHTML = "port";
            aval.placeholder = "123";
            aval.pattern = "^[0-9]+$";
            break;
        case "ICMPV4_CODE":
            lbl.innerHTML = "icmpCode";
            aval.placeholder = "123";
            aval.pattern = "^[0-9]+$";
            break;
        case "ICMPV4_TYPE":
            lbl.innerHTML = "icmpType";
            aval.placeholder = "123";
            aval.pattern = "^[0-9]+$";
            break;
        case "ICMPV6_CODE":
            lbl.innerHTML = "icmpv6Code";
            aval.placeholder = "123";
            aval.pattern = "^[0-9]+$";
            break;
        case "ICMPV6_TYPE":
            lbl.innerHTML = "icmpv6Type";
            aval.placeholder = "123";
            aval.pattern = "^[0-9]+$";
            break;
        case "INNER_VLAN_PCP":
            lbl.innerHTML = "innerPriority";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "INNER_VLAN_VID":
            lbl.innerHTML = "innerVlanId";
            aval.placeholder = "1-4094";
            aval.pattern = "^(?:40(?:[0-8][0-9]|9[0-4])|[1-3][0-9]{3}|[1-9][0-9]{1,2}|[1-9])$";
            break;
        case "IP_DSCP":
            lbl.innerHTML = "ipDscp";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "IP_ECN":
            lbl.innerHTML = "ipEcn";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "IP_PROTO":
            lbl.innerHTML = "protocol";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "IPV4_DST":
        case "IPV4_SRC":
            lbl.innerHTML = "ip";
            aval.placeholder = "1.2.3.4/32";
            aval.pattern = "^(?:(?:2(?:[1-4]\\d|5[0-5])|1\\d{2}|[1-9]?\\d)[.]){3}(?:2(?:[1-4]\\d|5[0-5])|1\\d{2}|[1-9]?\\d)/(?:(?:3[0-2]|[12]\\d)|\\d)$";
            break;
        case "IPV6_EXTHDR":
            lbl.innerHTML = "exthdrFlags";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "IPV6_FLABEL":
            lbl.innerHTML = "flowlabel";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "IPV6_DST":
        case "IPV6_ND_TARGET":
        case "IPV6_SRC":
            lbl.innerHTML = "ip";
            aval.placeholder = "1234::abcd/64";
            aval.pattern = "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))/(?:(?:6[0-4]|[1-5]\\d)|\\d)$";
            break;
        case "METADATA":
            lbl.innerHTML = "metadata";
            aval.placeholder = "0x12ab";
            aval.pattern = "^0x[0-9a-fA-F]{4}$";
            break;
        case "MPLS_LABEL":
            lbl.innerHTML = "label";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "SCTP_DST":
        case "SCTP_SRC":
            lbl.innerHTML = "sctpPort";
            aval.placeholder = "1-65535";
            aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
            break;
        case "TCP_DST":
        case "TCP_SRC":
            lbl.innerHTML = "tcpPort";
            aval.placeholder = "1-65535";
            aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
            break;
        case "TUNNEL_ID":
            lbl.innerHTML = "tunnelId";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "UDP_DST":
        case "UDP_SRC":
            lbl.innerHTML = "udpPort";
            aval.placeholder = "1-65535";
            aval.pattern = "^(?:6(?:5(?:5(?:3[0-5]|[0-2][0-9])|[0-4][0-9]{2})|[0-4][0-9]{3})|[1-5][0-9]{4}|[1-9][0-9]{0,3})$";
            break;
        case "VLAN_PCP":
            lbl.innerHTML = "priority";
            aval.placeholder = "123";
            aval.pattern = "[0-9]+";
            break;
        case "VLAN_VID":
            lbl.innerHTML = "vlanId";
            aval.placeholder = "1-4094";
            aval.pattern = "^(?:40(?:[0-8][0-9]|9[0-4])|[1-3][0-9]{3}|[1-9][0-9]{1,2}|[1-9])$";
            break;
        default:
            lbl.innerHTML = "Value";
            aval.placeholder = "value";
            aval.pattern = "value";
    }
}

function addCriteria() {
    var atype = document.getElementById('flowcrittype').value;
    var avalue = document.getElementById('flowcritval').value;
    if(avalue.length > 0) {
        switch(atype) {
            case "ETH_DST":
            case "ETH_SRC":
            case "IPV6_ND_SLL":
            case "IPV6_ND_TLL":
                avalue = "mac=" + avalue;
                break;
            case "ETH_TYPE":
                avalue = "ethType=" + avalue;
                break;
            case "IN_PORT":
            case "IN_PHY_PORT":
                avalue = "port=" + avalue;
                break;
            case "ICMPV4_CODE":
                avalue = "icmpCode=" + avalue;
                break;
            case "ICMPV4_TYPE":
                avalue = "icmpType=" + avalue;
                break;
            case "ICMPV6_CODE":
                avalue = "icmpv6Code=" + avalue;
                break;
            case "ICMPV6_TYPE":
                avalue = "icmpv6Type=" + avalue;
                break;
            case "INNER_VLAN_PCP":
                avalue = "innerPriority=" + avalue;
                break;
            case "INNER_VLAN_VID":
                avalue = "innerVlanId=" + avalue;
                break;
            case "IP_DSCP":
                avalue = "ipDscp=" + avalue;
                break;
            case "IP_ECN":
                avalue = "ipEcn=" + avalue;
                break;
            case "IP_PROTO":
                avalue = "protocol=" + avalue;
                break;
            case "IPV4_DST":
            case "IPV4_SRC":
            case "IPV6_DST":
            case "IPV6_SRC":
                avalue = "ip=" + avalue;
                break;
            case "IPV6_EXTHDR":
                avalue = "exthdrFlags=" + avalue;
                break;
            case "IPV6_FLABEL":
                avalue = "flowlabel=" + avalue;
                break;
            case "IPV6_ND_TARGET":
                avalue = "targetAddress=" + avalue;
                break;
            case "METADATA":
                avalue = "metadata=" + avalue;
                break;
            case "MPLS_LABEL":
                avalue = "label=" + avalue;
                break;
            case "SCTP_DST":
            case "SCTP_SRC":
                avalue = "sctpPort=" + avalue;
                break;
            case "TCP_DST":
            case "TCP_SRC":
                avalue = "tcpPort=" + avalue;
                break;
            case "TUNNEL_ID":
                avalue = "tunnelId=" + avalue;
                break;
            case "UDP_DST":
            case "UDP_SRC":
                avalue = "udpPort=" + avalue;
                break;
            case "VLAN_PCP":
                avalue = "priority=" + avalue;
                break;
            case "VLAN_VID":
                avalue = "vlanId=" + avalue;
                break;
            default:
                avalue = "value=" + avalue;
        }
        var abody = document.getElementById('flowselector');
        abody.insertRow();
        var arows = abody.rows;
        var crow = arows.item(arows.length - 1);
        crow.insertCell();
        crow.insertCell();
        crow.insertCell();
        crow.cells[0].innerHTML = atype;
        crow.cells[1].innerHTML = avalue;
        document.getElementById('flowcritval').value = null;
    }
    else {
        alert('Missing criteria value.')
    }
}

function removeCriteria() {
    var bbody = document.getElementById('flowselector');
    if (bbody.rows.length > 0)
        bbody.deleteRow(bbody.rows.length - 1);
}

function createFlow() {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/createflow', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var pdata = "";
    var flow = {};
    flow['priority'] = parseInt(document.getElementById('flowpriority').value);
    document.getElementById('flowpriority').value = null;
    flow['timeout'] = parseInt(document.getElementById('flowtimeout').value);
    document.getElementById('flowtimeout').value = null;
    flow['isPermanent'] = document.getElementById('flowisperm').checked;
    flow['appId'] = document.getElementById('flowappid').value;
    flow['deviceId'] = document.getElementById('flows-device').value;
    var treat = {}
    var instr = document.getElementById('flowinstructions').rows;
    var ins = [];
    for (i = 0; i < instr.length; i ++) {
        var ci = {};
        var crow = instr[i];
        ci['type'] = crow.cells[0].innerHTML;
        if (ci['type'] != "NOACTION") {
            var ival = crow.cells[2].innerHTML.split("=");
            ci[ival[0]] = ival[1];
        }
        if ( crow.cells[1].value != "NA" )
            ci['subtype'] = crow.cells[1].value;
        ins.push(ci);
    }
    treat['instructions'] = ins;
    treat['clearDeferred'] = document.getElementById('flowcleared').checked;
    flow['treatment'] = treat;
    var sel = {};
    var crit = document.getElementById('flowselector').rows;
    var cri = [];
    for (i = 0; i < crit.length; i ++) {
        var cc = {};
        var crow = crit[i];
        cc['type'] = crow.cells[0].innerHTML;
        var cval = crow.cells[1].innerHTML.split("=");
        cc[cval[0]] = cval[1];
        cri.push(cc);
    }
    sel['criteria'] = cri;
    flow['selector'] = sel;
    var instr = document.getElementById('flowinstructions');
    while (instr.rows.length > 0)
        instr.deleteRow(0);
    var crit = document.getElementById('flowselector');
    while (crit.rows.length > 0)
        crit.deleteRow(0);
    pdata += "flow=" + btoa(JSON.stringify(flow));
    xhttp.send(pdata);
    refreshGroups();
}

function deleteFlow(devid, flowid) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/deleteflow', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var pdata = "devid=" + devid;
    pdata += "&flowid=" + flowid;
    xhttp.send(pdata);
    refreshFlows();
}

function pcheck(elem) {
    if (elem.checkValidity()) {
        elem.classList.remove('is-invalid');
        elem.classList.add('is-valid');
    }
    else {
        elem.classList.add('is-invalid');
        elem.classList.remove('is-valid');
    }
}

// Timer
var timerId = -1;

function setAutoRefresh(timeout) {
    if (timerId > 0)
        clearInterval(timerId);
    timerId = setInterval(refreshAll, timeout);
    bt = document.getElementById('btn-timer');
    bt.setAttribute('onclick', 'stopAutoRefresh();');
    bt.innerHTML = "Stop auto-refresh";
}

function stopAutoRefresh() {
    if(timerId > 0)
        clearInterval(timerId);
    bt = document.getElementById('btn-timer');
    bt.setAttribute('onclick', 'setAutoRefresh(10000);');
    bt.innerHTML = "Start auto-refresh";
}
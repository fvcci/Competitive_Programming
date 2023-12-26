import sys
from icecream import ic
from collections import deque
from dataclasses import dataclass
from typing import Tuple
import re
from tqdm import tqdm
from math import gcd


def p2():
    global arr
    arr = arr[0].split(",")

    def hasher(label):
        cur = 0
        for x in label:
            code = ord(x)
            cur += code
            cur *= 17
            cur %= 256
        return cur

    def separate(val):
        a = val.find("-")
        if a==-1:
            a = val.find("=")
        assert a != -1

        label = val[:a]
        sign = val[a]
        if sign!="-":
            focal = int(val[a+1:])
            assert 1 <= focal <= 9
            return label, sign, focal
        else:
            return label, sign, -1

    ans = 0
    boxes = {i:[] for i in range(256)}
    for x in arr:
        label, sign, focal = separate(x)

        hash_val = hasher(label)

        if sign=="=":
            flag = False
            for i, (ylabel, yfocal) in enumerate(boxes[hash_val]):
                if ylabel==label:
                    boxes[hash_val][i] = (ylabel, focal)
                    flag = True
                    break
            if not flag:
                boxes[hash_val].append((label, focal))
        elif sign=="-":
            y = -1
            for i, (ylabel, yfocal) in enumerate(boxes[hash_val]):
                if ylabel==label:
                    y = i
                    break
            if y!=-1:
                del boxes[hash_val][y]

    ans = 0
    ic(list(filter(lambda x: len(x)!=0, boxes.values())))
    for _, box in boxes.items():
        for i, (label, focal) in enumerate(box):
            ans += (1+hasher(label))*(i+1)*focal

    ic(ans)


def p1():
    global arr
    arr = arr[0].split(",")

    def hasher(cur, val):
        code = ord(val)
        cur += code
        cur *= 17
        cur %= 256
        return cur

    ans = 0
    for x in arr:
        cur = 0
        for c in x:
            cur = hasher(cur, c)

        ans += cur

    ic(ans)


def main():
    assert len(sys.argv) == 3
    sys.setrecursionlimit(5000)
    TEST_INPUT_STATE = sys.argv[2]
    TEST_STATE = sys.argv[1]

    if TEST_INPUT_STATE == "test":
        inps = tests
    if TEST_INPUT_STATE == "prod":
        inps = prod

    global arr
    for inp in inps:
        arr = [s.strip() for s in inp.split("\n")[1:-1]]
        if TEST_STATE == "p1":
            p1()
        elif TEST_STATE == "p2":
            p2()


tests = [
"""
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""",
]


prod = [
"""
gt-,kdn=7,dzc-,rcdg=4,fvhz-,fjkx=1,bfx-,ntl=1,kll-,nngd=9,sr-,pqk-,tts=8,qtlz-,zd=6,jxm-,vbt-,vbt-,jr-,cgq-,tvs=8,dzq-,qmgfxs=2,qh-,fpcls-,cbx=9,jvr=6,td-,bx-,xg-,ndm-,mqnc-,th=5,sjx=7,rcdg=9,hsstf=5,mtskb=5,dpx-,nnh=1,rc-,jr=4,pbmq=5,cfj=2,gl-,nmj=3,dzq=6,xvp-,pszs-,jbd=5,xlh=1,jlvl-,bdds-,dmxqf=9,rqkqq-,nhvt-,zsj=1,nz-,xcxx-,nm-,jc=3,hlq=5,xcd=1,khk=7,fhl-,jmj=7,ccfg-,mnm-,rtn-,ck=1,vbn-,mg-,pcvhq=5,br-,gcz=6,gvv-,vlbzt-,kqc=3,bq-,rhmm=1,fprt=8,spq=2,rs=4,vm-,vdn-,ndm=8,dprthp-,xc-,bhn-,tzd=1,kggq=1,bchfq-,blh=5,tvs-,qsbn-,vqbmds-,dpx=3,tvs-,qsbn=7,fmk=3,ck=9,nmck-,nt=3,znlg-,nk-,pdnmg-,pxfmfv=5,mz-,zc-,drhg=9,hrr=1,cmzp=6,jvr-,jkfx-,cgc=6,gkhk-,qk=6,zh=3,tgk-,qvc-,sv=8,bc=4,lqvnj=4,dz-,gnxk=7,mptk=6,qg=9,qk-,vpjk=1,fcmk=3,rpl=1,dj=3,kf-,llnfd=3,hshl=8,gcz-,bmqz-,fs=5,brj=2,jgnm-,msfmm=6,xg=8,rqkqq-,jvl-,zpgzv-,zr-,lrh=1,vr-,vxc-,bl=1,vjxk-,lm-,zkvc-,dzc-,psq-,ddsg=4,cmzp=3,qp=9,tdfvs-,gjl-,kzv-,klfhc=7,tp-,zb=4,mxq-,rv=1,ffgvvh=7,rhmm=6,bd=7,ldc=7,gpq=4,qsbn=3,jr-,prsm-,tgk=6,vr=2,lblcs-,kll=2,pcm=7,ml=8,tvs-,dfr-,sfzcz=2,pjqc=6,jdv-,prsm=7,vn=8,pft=3,nz=1,vn=7,hmjg=9,jl-,jc=1,vkpgz-,xnzj-,jvl-,mtc=5,tdthvb-,lf-,jslp=4,tnxq-,mc-,tts-,qtlz-,jhq-,lblcs=2,ttp=1,hfqtc=1,vcp=6,jl-,tv-,pr-,cd=4,sn-,rtn-,xvp-,xq=3,cd=2,tp=1,lf=7,xkt=5,hk=5,ss-,mz=9,tbh-,plx=4,nzn-,bhn=9,mxmmk=3,cx=9,ldphj-,xzh=8,jkmf=5,kll-,vmtr=9,xbjb=7,ndn-,hfz-,msfmm=1,bvc-,skdr=2,cj=5,qkt=8,kj-,nx-,qnr=4,xkt-,kz=7,fhvt-,kcv=6,cpx=5,ndm=6,zkvc=1,pqk=6,pm=9,pcvhq=7,th-,kqc-,lblcs-,nngd-,pm=8,cj=8,jk-,tts-,lmcbt=5,pcvhq-,kjq=9,jkmf=8,qkf=6,zd=9,mrn-,jfv=9,dbkc-,nmj=4,mh=2,qsbn-,hh-,vltf-,nnh-,pmcpr=4,vjm=7,mz-,zpdm=2,hrpd=5,qr-,sthr-,mxmmk=2,xmqr=1,czx-,kcgvv=9,kk-,ghm=3,mrn=1,vcp-,gjl-,skk=2,mtc=1,tnxq-,xt=1,chv=6,jdfnb-,qshv=6,hlq=6,kxj-,bp-,vqt-,qmkzs-,jds=6,brx-,nhvt=1,blh=1,kxj-,rhmm-,tj=6,cd=1,mffd=9,zqj-,lfr-,bvc-,lhljjx=6,gdnmgb=1,cmzp=2,qvd-,jds-,mqnc-,tr=5,nt=9,sfzcz=2,pl-,gz-,fpcls-,xkt-,nfrn-,vmtr=7,qmgfxs=3,mv-,pjt=2,sgs=8,lpp-,pjqc-,ldc-,jslp-,rhmm=5,ss=4,bvc-,ltcr=9,hb-,srf-,stx=1,bchfq-,xts=6,cf-,jxsq-,rsxcb-,nx=2,kqjd=7,zqj=3,td=2,cgq=6,cpx=5,rp-,kj=3,mcs=2,ssjx-,xcd=1,gj-,brx=4,vnz=5,tjz=1,jlvl=2,bs=6,bzkz-,hb=3,hm-,kcgvv-,jvv=4,qrpd-,kxj=1,chkn-,cdbp-,qz-,mjl=7,fbb=8,htt=2,nhvt=5,rzrm-,hrr-,jr=4,rzrm=6,cv-,nnh=1,ggk=6,pjvc=4,lfr-,fq=2,vqt-,vzh-,gkhk=9,cmgtn-,chkn=6,jds=7,lblcs=1,sr=2,zsh-,ghm-,lz-,vg-,bc-,vbn=5,sv-,dqs=1,vbn-,vjzqb=4,fjkx-,pjqc-,ltpp-,mzl=7,ssn=9,bx-,ndm=1,vjm-,tgk-,vjxk=4,lt=4,dprthp=4,cjlm=6,jk=5,xcd-,pb-,djxm=8,zqj-,bqn-,czx-,hl-,bj=2,nlm=1,spq=4,kf-,ddsg=4,qmdxx-,hm=6,pm-,ntbsn=2,qd=3,mg-,bhn-,ssdg=1,kpv=4,bzkz=9,cbx-,jqd-,pcr-,kd-,pxfmfv-,cf=8,dpjtlc=7,gl-,rtn=4,gxg-,bzkz-,hshl-,vnz=6,sgd=5,vc=6,blh-,bdds=8,fcmk=5,dfr=6,nk=2,jtlk-,jkfx=5,rzrm-,cvk-,stx-,ssjx-,qmkzs-,tp-,nsvq-,bksx=4,tj=5,xg=3,lccp=2,xg-,ntbsn=4,qvc=7,nbmh=1,cx-,dbkc-,sndj-,vfc-,zd-,nr-,hspb-,gj-,xts-,hshl=6,gv-,csb=8,cv=5,vqt=6,pmkh=2,kr-,pb=6,tdfvs-,fmk=6,fh-,fbt-,vjzqb=5,lm=6,msqrl-,kzv=8,gj=3,kcv=3,ffcltb-,jxsq-,kggq=4,zf-,lccp-,hhhbhd=9,nnh=2,nngd-,hhhbhd-,xkt-,nt=8,cvk=9,srf=5,tv-,mf=5,ss=8,tzd-,ll=9,lz=7,qmdxx=1,pdls=6,dpjtlc-,hsstf=9,kqjd=1,msfmm-,qr-,tzx=6,mqv=4,mqnc=8,jvv-,tvs=1,tts=7,cdbp-,vnzlsj=8,dstpv=6,nbqkzl-,mtskb=4,vqt=6,vl=5,vqt=8,bxs-,hrr=4,jdfnb-,khk-,cmzp-,sgs-,chcgr=7,mcs=1,lx=2,drhg=5,mnm=5,tvs-,ndm=7,csb-,klfhc-,msfmm=5,hhj-,mhnmg-,pc=5,jhq=9,spqgbb-,kd-,qmgfxs=2,pjvc=2,mxq-,frd=4,ll-,jhq=4,sstzdv-,tqzl=3,kr-,dk=4,gt=9,dpjtlc=9,jmqcnd-,jgnm-,ld=4,gf-,bqn=5,cs-,nbmh-,pl-,mptk-,pcvhq=4,cbx=9,ltpp-,zpdm-,nx-,vqt-,tz=6,grb-,bksx-,fpcls=6,tzd=1,rp-,vbt=4,kqc-,vg=6,czv=8,zpgzv-,td=8,xkq-,hk=2,qp=9,zpgzv-,gl=7,mxmmk-,fkpl=3,xt-,bzqqc-,ld-,gjl=9,sgd=1,dkz-,mqv-,zsb=5,zjknb=6,vq-,fmnz=7,jvl=7,hl-,rmb=5,dvr=1,nm-,nbmh-,ntbsn=7,bxs=5,nsvq-,sc-,jqd=2,qbk-,ndm-,hfz-,bj=4,td-,sgd=3,tts=1,msfmm-,qk=2,dnksd-,kk=5,gvt=9,vnrz-,zpdm-,lll-,fpn=2,ffcltb=8,bc-,tqzl-,hq-,bs-,qmdxx=4,dstpv=8,drhg-,qd-,czv=7,bl=2,dv=6,ltcr-,zh-,vkpgz=7,bvc=9,hr=6,pszs-,czv-,qx=7,srv-,fcmk=5,klcz-,xg=7,vfc-,zpk-,qz-,dgt-,ct-,kqjd-,kff-,khk-,jcv=3,mffd=5,zf=1,gj-,ltpp=4,hsstf=1,tdfvs-,zfbl=9,hk=3,tm-,gvv=2,jcv=1,fprt=5,clzn-,th-,fhl=1,mz=3,tz-,rh=6,csb-,cj-,xlh-,qz=2,vfc=6,nm=8,vfc-,xts-,lrh-,ntl-,xn-,gf=6,jkmf=8,sgs-,fhl-,tgr=9,hhhbhd=6,kd-,dzc=4,vcp=9,lj-,hkr-,kcc-,cjv=7,ll-,ssjx-,brx-,xfm-,hb-,jvv-,vq=8,hb-,pb=3,cvk=7,znlg-,vcp=5,nnh=1,pft-,zr-,ntbsn=8,vxc=5,bmqz-,xg-,cvslb-,jk=6,vlbzt-,hspb-,vmtr-,lqvnj=2,fbb-,jr=8,hmjg=7,tpx=6,frd-,mf=8,kqjd=1,bqn-,zpdm-,xg=1,klfhc=3,znnhs=2,fcmk-,qqv-,gt=3,nfrn-,lg-,qc-,rhmm=3,tgcznv=7,qnt=3,jds=5,gvv=3,xts=1,cjlm=3,cct=7,xts-,fn=9,mqnc=2,dbms-,kpv=2,jds=9,msqrl-,jdfnb-,gtgflc=5,mc=6,jds-,kll=4,vfc-,sndj=5,xt-,jkmf=5,lll=6,dnksd-,hdk-,qqj-,nzn-,srv=8,hsstf-,xnzj=5,pcr=8,qx=9,pbmq-,cbx=5,sc=4,pv=2,zd-,kdn-,nz-,qh=8,gtgflc=3,rmb=7,gqpr-,tgk-,klcz=5,gxg=6,gc=9,bs=4,mtskb-,psq=5,cfj=5,bqn=6,xbb=2,cvslb=8,zf-,lmcbt-,ffcltb=6,jlvl-,ns-,gkhk-,ckdl-,ss=4,hcz-,vjxk=7,rpl=1,gj-,ngt=8,qrpd=9,lz=5,nfm=6,lj-,mcs=8,mjcl-,jk-,fdmbjx=7,kll-,mjcl=2,xn-,dmxqf=6,jd=5,pmkh-,tts=7,bb-,xvp-,jk-,pl-,ddsg=2,ghm-,qq-,htxd-,qkf=9,cjlm=2,nzq-,bksx-,cjlm-,sstzdv-,bqn-,qqv=5,kcf-,pqk=1,cmzp=6,vmtr-,xcxx=9,dk=4,bzkz=4,sjx-,fmnz-,gkhk=4,ljczkh=1,gng=3,tgk-,pf-,gk=2,skk-,ld=7,sgd-,dmxqf-,ddsg-,gv=9,dkz=6,dbms-,bfx=6,ss=5,gvt-,tdfvs=2,mk-,fcmk-,cx-,hh-,gk-,dcdj-,xkq-,ck-,grp=9,cgq-,qsv=5,tp=2,pnh-,brx=8,dgt=6,mtr=4,gkhk=2,rhmm-,hhhbhd-,cvk-,nzn-,rp=6,st=6,nk-,xn=1,lm=3,sstzdv=9,mzl=4,hvxbfz-,qp-,qz-,mv-,kd=2,cb=1,kcv=2,qsv-,grb-,dnksd=7,mtc-,dcdj=4,ct-,lccp-,lqvnj=4,khk=5,qjfj=4,qnr-,lqvnj=6,nsvq=4,vbn-,kdn-,pcr-,sn=1,cs=8,cvslb=3,pbmq=5,kz=3,clzn=2,rp=3,tl-,mz-,tbh=6,chv=3,ld=4,vx-,mcs-,pft-,rcdg-,lk=4,nx=2,pcm-,fhvt-,nk=1,dbms=7,nlm-,hrpd=4,ghm=7,cf-,mtskb-,jgnm-,cct-,mkq-,zpgzv-,ggk=2,clzn=5,pft-,cj=6,qqj=4,mk=6,hr=6,nglp-,hvxbfz=5,qc=1,hq-,qvd=2,brj=7,ssxq=2,tb-,lll=1,cs-,xcv=8,skdr=2,lfr-,jmj=1,gqpr=3,pcvhq-,hkr-,srv-,cpx=9,plx-,gvv=2,mq=1,kqc-,spqgbb-,zsh=6,kjq-,jlvl-,gqpr-,rc-,xlh-,vc=3,bnvn-,mjl=6,ppt=4,kcv=3,lg=4,pdls=5,gt-,bs-,kggq=6,ns-,zsj=2,blh-,ffgvvh=8,tpmkq=1,lk=4,dj=3,jvl-,fmnz=4,vx=6,grl-,nglp-,qq-,qd=4,prsm=2,ss-,tbh-,mcs-,vr=3,dmxqf=6,mffd-,vjxk=1,vbt=6,kr-,pf-,nmck-,tr-,zd=3,zpdm=4,pnh=4,dbms-,kd=2,qjfj-,tgr=2,fbt-,lqvnj=3,gk=1,nj=6,fm-,fh=6,pszs=1,jd-,nknth-,bmqz=6,hsstf-,prrp=2,llnfd=6,mkq-,jvv-,mnm=9,xnzj-,nhvt=6,ghff=5,gvt-,klcz=1,prrp=6,mxmmk=8,chcgr-,tgr-,xkq=3,qn-,kr=4,gl-,sfzcz-,kcf=2,th=6,lvv-,jcv-,klcz-,mrn-,qc=4,sgs-,prrp-,prrp=3,msqrl=4,mnm-,zjmhlp-,xmqr=2,kp-,hvxbfz=7,bs=8,ml=8,kvp=1,hfqtc-,xcxx=3,zsb=5,rhmm-,qd=3,fpcls=2,gbr-,dxj-,czv=8,kcc-,kj=3,xq-,jslp=3,dzq=6,ntl=4,dkz=2,cjlm=4,bgnt-,gbr-,chkn-,dv=1,htt=6,cxmkv=9,fjp-,zc=8,dxj=6,mtc=2,mptk-,zt-,trp=7,cjv-,czx=2,kff-,tts-,ssn=7,lk-,tm=5,xn=4,td=7,qg-,zjmhlp-,jkfx-,hhj=4,khk-,gt-,qbk-,nfm-,ddsg-,chm-,qqj-,qh-,qkf=4,cd=8,kcc-,xmqr=4,vnz-,qgjvgz=3,sfzcz=3,mjcl=1,fpn-,dbms=5,dxj=7,zpk-,lpl-,lt-,gk-,bfx=7,bxs-,xq=3,cvslb=2,nz=3,kz-,tjz=1,dpx=5,vxc=5,dnksd-,gbr=9,bl-,rqkqq-,llnfd-,dcdj=2,pv-,zt-,skdr=7,frd=2,tzx-,bfx=6,jgnm-,vjzqb-,tts=2,cf-,pdls-,cmgtn=7,hshl-,skdr=5,vkpgz-,dk-,djxm-,dvr-,vjxk-,czx=7,hrr=8,bgnt=4,gqpr=3,hm-,bx-,xzh-,nxn=4,clvjf-,zc=3,zb-,mk=6,mq-,prrp=2,ztqq-,zc-,pjqc-,tzd-,jd-,hspb-,dvr=1,fkpl=6,xq=1,xbs-,vpjk-,zsj=6,ffcltb=7,gj=2,rqkqq-,htxd-,kj-,nxn=9,pqk-,mc=4,qz-,zfbl-,chcgr=1,xnzj=9,dfr-,zfbl=1,tgcznv-,xcv=1,ss-,bksx-,pv=3,vlbzt=3,ddsg=5,pf=5,gxg-,pcm=8,ndn=9,chv=4,gnxk=4,hb=2,vbt-,hfqtc-,tbh-,dcdj=5,qc=2,prsm=2,mj-,srf-,gtgflc=1,pdls-,fzhzsp-,xj=5,mc=7,xmqr=7,pnh-,tpmkq-,chkn=2,xg=6,bq-,fmnz-,ddsg=3,frp=3,mqnc-,zt=2,lk=2,gcz=3,kr-,dpjtlc=2,mtr=4,hhhbhd=5,cdbp=4,qmkzs=3,qrjvc=1,ml=5,kqjd=5,qgjvgz=8,gbr=2,vnrz-,zkvc-,qx-,xcxx-,fvhz-,xn-,qkt=3,zfbl=2,pr-,vzh=4,jfv-,mj=4,lg-,nlm-,qkf=3,vn-,kcv=2,jcv=3,lfr-,zt=6,xcv=6,zd-,lrh=6,gj-,tl-,cj-,tzd-,hhj-,ppt-,zpdm-,vm=9,ljczkh-,vkpgz-,vnrz=4,clzn=7,tm-,gt=7,pm=5,qx-,tts-,cvk-,fbb=4,cgc-,jmqcnd-,bp=2,sdznb=9,rp-,lmcbt=5,qjfj-,clvjf=2,pbmq=5,bksx=8,bxs-,clzn-,vn-,cmgtn-,gpq-,rhmm-,fvhz=9,gl=7,tvs-,lpl=2,grb-,fkpl=5,czv=8,klcz-,fmk=7,lrh-,mptk-,klfhc=7,qkt-,nz-,th=6,fq-,skdr=5,pv=7,pr-,tts=1,lz-,hm=3,klcz-,rpl-,jhq=5,rcdg-,qrjvc=2,dv=8,nm-,kggq-,dqs=8,msqrl=6,cvslb=8,qvd=1,dk=2,skk-,fv-,jvv=7,vx-,lqvnj-,nglp-,pnh=8,mmq-,plx-,nknth-,sfzcz-,sndj=2,pjt=2,kp-,gf-,zqj-,lfr-,jqd=4,qrjvc-,mjl=5,drhg-,pjt=8,zf=9,tv-,hfz=4,tdfvs=2,vqbmds-,tgr=3,zpdm-,fjkx-,tgr=3,rtn-,dprthp-,ldc=6,ghm-,mj-,gpq-,lqvnj-,lt-,qn-,ngt-,qrjvc=5,czncl=6,hmjg-,nk-,xc=4,lll=7,qkt=5,xbjb-,th-,hlq-,lqvnj=4,cx=9,dk-,mxq-,khk-,fv=2,gt=8,pjqc-,jgnm=2,xfm=7,qvc=1,br=9,ljczkh=1,jqd-,kxj-,gqpr-,pft-,fhl=9,bj=5,bvc-,vc=2,hhj-,kr=1,bhmp-,zf-,vjm=1,khk-,vzq-,vqt=3,czncl-,mzl-,ldc-,pm-,khk-,mqv=6,dk-,grl=6,tb-,jvr-,tm=9,sstzdv-,ppt=3,hfz-,tl-,hhhbhd-,rv-,nsvq=6,ckdl-,zfbl-,mqv-,ld-,pcr-,czx-,mqnc-,gbr=3,jfv=8,gxg=3,qrpd=9,qqv=4,sgd-,jvv=7,djxm-,gl-,bp=9,cs=7,sndj-,xj-,td=1,grl=9,sgs=3,pdnmg-,kf-,qc-,hsstf-,bj=5,kpv=4,rv=5,nt=9,ndn=1,mrn=5,qnt-,zb-,zpdm=8,dz=3,qgjvgz=1,cmgtn-,cb-,gj-,vpjk=2,qh-,ct=6,dqs=7,hqfmx=9,xzq-,llnfd=9,zt=8,zjknb-,qgjvgz=7,nzq-,mtc-,pft-,lt-,nknth-,rzrm=7,fh-,pdnmg=3,gng-,bchfq-,nsvq-,kvp=7,lf=1,fjp=5,jdv=1,lf-,qx=4,znnhs=8,bx=7,kzv-,sgs=7,mhnmg-,nx=6,xvp-,sn-,bx=9,zfbl=4,sstzdv=3,zsh=1,ztqq=6,qc=4,plx-,xkt-,zn=2,hm-,ghm=6,vl=5,ccfg=6,pjt=1,zn-,qn-,spq-,xvp=6,pb-,msqrl-,tpx-,qr=1,pcvhq=3,znnhs=4,qgjvgz=1,cct-,glv-,cd-,bvc=6,hvxbfz=8,fq=7,zf-,cgq-,qr-,hcz-,bzqqc=4,pc=6,cbx=1,dj=3,kjr-,bzqqc=3,sjx-,sstzdv-,qjfj=7,mtskb-,jtlk=9,dvr=7,cv-,nsggjg-,kpv-,hdk-,qg=4,dbkc=1,bhmp-,bfx=7,dbms=2,kzv=6,np-,prsm=6,gj=2,grp-,br=1,vlbzt-,mmq-,vlbzt-,pl=7,gkhk=2,rs-,mxmmk=5,rsxcb=7,qnt-,hrpd-,klcz=2,xg=6,tpx=5,lpp=8,xcd=7,qp-,pcm-,ck-,bmqz=1,xbjb-,pjt-,bqn=6,dgt=3,rzrm-,bd=7,zfbl=9,hm=9,dbkc-,mhnmg-,bhn-,vnz-,gj=5,ffcltb=6,qd=5,hspb-,cmzp=9,qrpd-,ngt=2,bksx=1,xbs-,bx-,ltcr=9,spq=4,kr-,fvhz=6,cgq=6,fbb-,st=2,cpx-,ztqq=3,nmn-,zc-,xkq-,ld-,kqc-,xg-,jxm-,bdds-,rqkqq-,jdv=8,rpl-,bqn-,pf-,qtlz=5,czv=7,nngd-,tdthvb=9,nj=5,jtlk-,nzn-,rsxcb-,spqgbb-,tr-,nzn=1,xlh=1,vn-,xcxx=3,ntbsn-,vpjk=2,mj=5,df-,brpr-,znlg=2,qd-,mmq-,qtlz-,hh-,lll=9,dstpv=8,jr=8,hm-,brx=7,tjz-,glv=1,ghk-,vltf=2,rp-,pr=8,vq-,mqv-,qrpd-,qsbn-,brj=1,qmdxx-,pcvhq=4,nbmh-,cct=5,stx=8,lrh-,qmgfxs-,zsj=3,kjr=1,ndm-,vl=5,dpjtlc=3,rsxcb-,ndn-,frp=4,xg-,ml=6,qshv-,zsx-,pr-,nt=5,qshv-,fj=4,pv=8,xnzj=1,djxm-,jqd=4,xt-,bdds=6,pdnmg-,pb-,rs=4,gz-,plx=7,lpp-,bchfq=8,kp=1,mffd-,xfm=4,vmtr-,fn-,pqk-,jds-,mqv=3,xcd=4,znlg=9,dkz-,kk=5,xfm-,kpv=3,lj-,zb-,rhmm-,mptk-,gkr-,lvv=1,gc-,kd-,tz-,cmgtn=2,tdfvs-,bksx-,qvd-,pszs-,rsn-,jqd=5,hhj=6,sdznb=5,qn-,vmtr=8,ggk-,lf-,ssjx=9,zh=6,mmq-,kjq=2,ljczkh=3,zpdm=8,brx-,qvc-,zfbl=3,dkz-,kll=3,bs=3,cj-,czncl-,ldphj-,sc=7,psq=6,rj=3,hvxbfz-,lj-,cv=6,gf=5,vx-,bx=4,ddsg-,rzrm=7,kj=9,lxl=5,pn-,htxd=5,czx-,sthr-,kzv=4,nz-,pszs-,kff-,grp=4,bgnt-,lll=8,nbmh-,frd=7,cvslb-,ztqq=6,bgnt=9,fvhz=6,grb=3,nzn-,pn=2,gdnmgb=3,pbmq-,skk-,fpn=2,ghm-,qsbn=9,xzq-,tzd=5,cct-,qtlz-,ll=1,hshl-,jmj=2,cpx=7,lqvnj-,dkz-,cvslb=7,mkq=7,hbl=2,kqjd-,bj-,pb=3,mv-,mtskb-,qsv=4,sc=8,lt=6,mhnmg-,jmqcnd-,fn=7,cpx-,pbmq=8,xt-,hq=5,nmj-,cmzp=5,nk=7,dp-,pjvc=9,sdznb-,kzv=7,mq-,glv=5,fm-,lx=8,vzq-,qp=1,dfr-,kggq=9,dgt-,ffgvvh-,pr-,kdn=1,hr-,ll-,qqv=7,qrpd=5,nzq-,tgcznv-,kdn-,pcr-,dmxqf=6,dbms=7,frd-,vq-,vq=3,drhg=2,hkr=8,cxmkv-,bq-,zpk=5,vnz=5,rcdg-,bnvn-,nr=7,bd=4,tbh=4,fmk-,xcd=2,hrr-,mtc=4,bb-,gdnmgb-,nlm=1,sthr-,vcp=8,ttp-,bhmp-,ffgvvh=4,sgs=5,bqn=9,kpv-,hhj-,rsxcb=4,rc-,df-,ntbsn=1,zfbl-,pjqc-,nsggjg-,mnm=5,fvhz-,frd-,sc=2,dgt-,qtlz=3,zpgzv=6,fbt-,nf=7,grl=7,kqc-,tqzl=7,hmjg-,cd=1,bksx=3,mkq-,sthr-,jslp=6,gqpr=4,vqbmds-,nfm-,nzn=7,dbkc-,ssdg-,mc-,dqs=8,czv-,dqs-,ppt=7,dstpv-,rzrm-,mtr=4,vc-,vqbmds-,kcf-,mffd=4,frd-,tqzl-,tzx-,chm=2,dz=5,pmcpr-,qmdxx-,lz=3,nmj=6,nzq=8,srf=8,bq=5,mnm-,pjqc-,cb=5,gdnmgb=3,fvhz=4,mrn=9,qbk=2,pn=4,pjqc-,dv=5,vjzqb=7,vrrdf=5,gz=7,dqs-,kff=5,kz-,gk-,ghm=7,sstzdv=8,vjzqb=9,bxs=9,kqjd-,nmj=7,skdr-,nmj-,vrrdf-,cs=8,vmtr-,mqnc-,nfm=1,gpq=1,sstzdv-,bmqz-,ld-,zb-,jdfnb-,mq=2,zd=3,cxmkv=4,lccp-,qnr=8,gnxk=4,ddsg-,tgk=3,vr-,fq=2,td=8,qsbn=5,pqk-,grl=6,xmqr-,rs=8,jfv=9,vnrz=8,ll-,bx=5,glv-,dqs=3,vn=8,dbms-,qshv-,fbt=1,kz=9,dcdj-,tv=8,hmjg=5,mf-,pjt-,zpk-,qsv=7,zfbl-,srf-,cd=1,prsm=6,qbk-,qnr-,bhn=3,jgnm=8,bl-,fm-,zd=3,vjzqb-,rc=5,th-,hmjg=8,cvslb=5,tj=6,bxs=3,mzl=3,rc-,vjzqb=8,zfbl-,glv=5,jtlk-,fpn=3,pcvhq=5,zjknb=1,ttp=8,qgjvgz=7,vnrz-,ld-,jmqcnd-,prsm-,frd=4,pr-,cmgtn=5,nfrn-,lhljjx-,vc-,dxj-,tjz=7,djxm=3,pmcpr=5,pdls-,pft-,zb=7,tjz=3,xvp-,nsggjg-,gvv-,grb-,pb-,zpk=7,skk-,clzn=3,lpp=2,lhljjx=4,mjcl=8,qmkzs-,jd-,bd=5,qsv-,ssjx-,vm-,jl-,hhhbhd-,zsj-,ttp=3,dbkc-,ghk=3,jfv-,hhhbhd-,qnt=8,sjx-,vjxk-,rsn-,vg=2,qqv-,qr=2,hmjg=5,ffgvvh-,pcr=7,fbt=5,vrrdf-,hq-,skdr-,kcv=3,mqv=3,mqnc=2,fv=2,nmj=1,rpl-,dkk-,pm=1,kp-,pft-,cv-,grl=6,glv=7,czx-,kdn-,hfqtc-,vc=2,hrr=3,vc-,ddsg-,jbd-,hmjg=3,vmtr=4,vcp-,brpr=3,rp-,tjz=5,sv-,chcgr=6,lz-,lj-,lrh=7,qmkzs=5,chkn-,rs=2,fdmbjx=5,nbqkzl-,kdn=4,qrpd=6,nbmh=8,tz-,gvv=3,hfz=5,cmgtn-,klcz=8,jcv=1,cxmkv-,chm-,tb-,jdfnb=1,nnh=5,dk-,czncl-,mrn-,vfc-,nzn=5,vqt-,czv=9,vl-,lf-,vzq=2,xbjb=6,nm-,hhj=4,spq-,zpdm=2,tz=1,nfm-,bj=1,vkpgz=3,htxd=4,hshl=9,vdn=1,bq-,sc-,tqzl-,tr=8,kr-,hvxbfz-,bzkz-,kggq=6,pcr-,xzq-,xcv-,dpjtlc=1,sgd=3,hhj=7,zn-,lmcbt=5,jvl-,bp=7,rtn=3,qc-,lblcs-,pjqc-,cd=9,rc-,nr-,lm-,zf-,fbb-,qtlz-,nbmh-,xg=9,kzv-,cmk-,zpdm=4,gk=9,zjmhlp=4,jk=3,lpp-,gqpr=9,kj=1,fj-,trp-,np=4,gbr=2,ffgvvh=7,gkhk=3,grb-,lf-,dj=6,mrn=9,vlbzt-,gqpr-,hvxbfz=2,mffd-,xcxx=5,bq-,lhljjx=6,dxj=7,nj-,pcr-,khk-,lxl=1,kdn=3,hspb=8,xmqr=2,xcv=4,cv-,gkhk=9,thm-,zf=6,rtn-,srv-,zd-,ssxq-,dbkc-,bchfq-,fbb=2,gbr-,tvs=3,vjm=4,hb=8,znnhs=9,sgs-,gz-,ndn-,ld-,qnr=5,vxc=8,mxq=4,clzn=2,sgd-,dfr-,sthr-,fvhz-,vzq=2,jkmf=8,bzqqc=9,cct-,vlbzt=2,pxfmfv-,brx=6,hh-,xlh=9,hshl=7,fjkx=5,frp=6,nmck-,xbb=9,mjcl-,sgd=3,ttp=9,kcc-,zn=6,jvr-,pm-,nsvq=3,fv-,kj-,sdznb-,sc-,ss=2,vkpgz=7,cgq=7,jtlk-,pb-,qn-,fbb-,pl-,ck=6,zqj=8,fn-,prrp=2,qz-,zsj=1,xlh-,cgq-,xg=5,pr=8,ss=9,csb-,nx=5,rmb-,xnzj-,bdds=4,sstzdv=8,lll=3,klcz-,fq-,kggq=5,hrpd=9,gj-,nzn=4,kcc-,thm-,fdmbjx-,bgnt=6,dprthp=7,vrrdf-,lx-,thm=3,vfc=8,th-,pxfmfv=1,cdbp-,gl-,cjv=9,lt-,ll=1,tdthvb-,frd=9,cvk=4,msfmm=6,mtc-,hcz=2,tqzl-,xq-,vm-,bq=4,jqd=4,tm-,jvl-,ndm-,mmq-,tdthvb=7,bc-,cx=3,gng=8,pqk-,kz=5,jd-,cx-,mkq=5,xvp=4,mxq-,hfqtc=9,vjzqb-,fbt=9,tdfvs=8,lvv=1,bj-,bzqqc-,tdfvs=2,rmb-,qn-,vpjk=2,vxc=9,ssn=5,ml-,fpcls-,sc=7,hfqtc=1,pjqc=9,pmkh-,cgq=2,gk-,bfx=9,vzq-,kk=8,vxc-,ck=6,nzq=3,tqzl=5,tjz-,nnh=5,hrr-,cfj-,sgd-,qvc=2,td=1,kxj-,gtgflc=8,vlbzt-,br-,ck=2,xfm-,vlbzt-,xq-,kzv=3,jslp=4,grb=7,gtgflc-,gf=2,xbs=4,nzq=6,gng=4,jfv-,np=8,brx=3,djxm-,kk-,dxj-,lrh-,xj-,hfqtc=3,sndj-,bc=2,ssn=1,fj-,hlq-,cmzp=9,jdfnb=1,ghm=9,znlg-,td=2,dj=9,sgd-,pm-,xvp-,dkk=1,lj-,bchfq-,tgcznv=3,qshv-,vkpgz=7,cgq=7,zsj=1,hm=9,ss=4,lxl=1,sc-,hbl-,tvs=9,gz=5,mj=9,jfv=2,gvt-,bksx=7,nlm-,pv-,mj-,zsj=1,bxs=6,clzn=6,chcgr-,tpmkq=4,qbk=5,kqc=7,sndj=3,djxm-,mnm=3,nm=4,ggk-,zb-,plx=1,vlbzt=4,bvc=4,nsggjg-,hrpd=4,kd-,srf-,xcd-,kdn=4,gv-,dp=3,gl-,cvk-,nngd=8,np=1,vdn=3,czncl-,hhhbhd-,rhmm-,mc=8,lxl=7,gv=9,kf-,bfx=2,gcz-,qshv=9,kcc-,gvv-,zkvc-,jhq-,ck-,hrpd-,vnz-,jd=7,stx=8,rqkqq-,bl=7,klcz=9,cmgtn-,gbr=5,ldc-,lf=5,fhl=8,gz-,qgjvgz-,qr=8,vlbzt-,blh=4,skdr=3,nnh=6,fpcls=6,zpgzv-,ndn=5,qkt=9,gpq=8,gvt-,cgc-,qx=8,fv=4,sgs-,skk-,mhnmg-,qnr=2,vnz-,ssn=3,jdfnb=7,zr=5,cgq-,qmgfxs-,ggc=7,qjfj=9,tzx-,nsggjg=3,gj-,qg-,ckdl-,ztqq=8,nt-,kp-,fbb-,gk=1,dv-,xts-,xvp-,dprthp=9,nj-,hl=7,pcr-,hmjg-,xzq=5,lrh-,qvd-,jtlk-,jlvl=3,sthr-,xcxx-,bzkz-,sjx-,jl=9,cmgtn=2,jmqcnd=6,bb=7,rp=4,xmqr-,srf=5,gbr=8,gpq-,gf-,tqzl=3,qtlz=6,prrp-,glv-,lqvnj=5,lpl=5,jqd=2,nsggjg=5,kqc=6,dbkc-,brx-,tgk=8,nbmh-,xcxx-,vxc-,lt-,gng-,tqzl-,fdmbjx-,ppt=8,gvv-,pnh-,pjqc=1,ml=3,pszs=7,dpjtlc=8,mmq=9,cfj=8,cx=8,tbh-,xzh=1,bvc-,pn-,nbmh-,mnm=6,czncl=8,fprt-,tr-,grb-,fq=8,th-,mq=8,pbmq=4,qkf=7,mk=4,vg=7,fq-,jvr=7,lqvnj-,jvl-,ffgvvh-,qjfj=1,nfrn-,cs=4,kz-,lt=4,fdmbjx-,clzn-,qc-,zpk-,jd=8,gdnmgb-,nknth-,ssjx=8,hvxbfz-,jvl=9,dbms=3,zsb-,fj=3,czx=9,lqvnj-,jl-,grp=7,pmkh-,lvv-,hspb-,hshl=8,qkt-,dv=9,ggc=1,bp-,bd-,xq-,tpmkq=3,qbk-,nbqkzl=6,brpr-,spq-,fmnz=2,bd=5,vfc-,czv=5,kggq=2,tdthvb=5,mtr-,hshl=7,cvslb=4,dv-,nmn=5,jds=2,zjmhlp-,qmkzs=1,spqgbb=2,xj=4,ss=1,rsxcb-,jlvl-,ndn=9,vsl-,rv-,fhvt-,nt-,qnr-,hbl-,pxfmfv-,nj=7,lt-,cv=3,gl-,lqvnj-,lx-,sv-,qc=7,jlvl=9,nr-,nf-,jk=5,gkhk-,xq=3,gxg-,vnz-,cxmkv-,xbb-,dmxqf-,gnxk=3,tgcznv=1,qkf=7,jtlk-,brx=8,pft=7,ntl-,gbr=3,lg=9,hr-,vzh-,ggk-,pqk-,pmkh-,qmgfxs-,gl-,ndn-,nj=8,vmtr=6,cgc-,gt-,pjt-,clvjf=2,dbkc-,zpdm-,zjknb-,dpjtlc-,hlq-,stx=9,mnm-,zn=3,mg-,mptk-,zkvc-,stx=4,jtlk=5,klcz=4,qsv=7,ngt-,grb-,lx=4,cbx=8,jbd-,grb-,vr=1,kff=5,frp-,ggk=2,xcv-,kggq=9,jl-,sv-,td-,fprt-,dzq-,lhljjx=5,ltcr=9,qq=9,dkz-,fq=9,dqs-,gkr=4,msqrl=5,ld=1,mv=5,bb=3,nbqkzl=1,nsvq=5,nbqkzl=6,ccfg-,czx=9,pjt=1,cmgtn=7,kk-,lfr=8,pjqc=6,xn=1,kxj-,vnz=3,cmgtn-,fpcls=6,qbk=6,kdn-,sgd=6,fpbm=7,qh=1,nlm=8,dvr-,czx=2,xcxx-,htt=1,qc=5,jvl=8,fn-,jkmf-,jkmf=4,gkhk-,bhmp=6,vc-,lg-,xj=7,cjv-,zsx=3,pb-,gng-,xn=1,vkpgz=3,khk-,bp-,plx-,qk-,xcxx=7,vdn-,fs-,qmdxx-,xn-,psq=6,kjr-,fh-,ddsg-,gl=6,kqc-,fv-,ggk=5,jl=9,cgc=6,mtskb-,mjl=5,sc=3,qrpd=9,jl=9,vzq=1,vcp-,jxsq-,bmqz-,vdn-,tgr=7,vkpgz-,dzc=9,zb=2,hr=2,pqk-,dnksd-,rcdg=6,pl=8,xbb-,lm-,fpbm=4,clzn=1,pc-,pjqc=4,xbjb=1,vqbmds=7,pmcpr=8,vrrdf-,jgnm-,skdr-,srv-,zt=5,gk=7,mhnmg-,czncl=8,nngd-,mh-,dbms=4,spq-,rpl=4,rc=2,qqj-,jmqcnd-,vfc=5,dgt=8,pl=7,kqjd-,tpmkq=5,vx=1,cpx=7,nzq=3,nxn=1,rzrm=4,fmnz=7,qtlz=9,tdfvs-,zh-,gz-,vkpgz-,bhmp=8,qqj-,fq=7,xkq-,qqv=2,hfz=2,kpv=9,bhn=1,nfrn=3,zkvc-,xbjb-,mjcl=2,dt=2,cdbp-,drhg-,kggq-,gng-,nmj-,brj-,qvd=6,mjl-,kzv=6,df=6,ndm=5,dk=9,fjp=2,nm-,rzrm=5,lpp=7,fbb-,gpq=4,cxmkv-,gbr=9,jslp=4,stx=2,mtc-,mz=8,kd-,kj=9,brj=9,qrpd=3,jvv=7,fzhzsp=8,psq-,cqjzm=6,tz-,qmgfxs=1,nj=9,cgq=2,dkz=3,lmcbt=6,gjl-,cfj-,xt-,vbt-,qvc=9,nhvt-,fjp=9,msqrl=2,mg=9,tgk=7,dz-,lg=9,qbk=1,rpl=9,lmcbt-,cjlm-,hk=9,mmq-,zsh=7,ld=1,kdn=6,gz-,hshl-,xlh-,pqk=1,sjx=9,nfm-,pmcpr=5,zb=6,cs-,jvl-,fvhz-,srv-,nglp=2,nsggjg=7,mtr-,qqv=6,lhljjx=6,qrpd=7,gz-,czv=2,dj-,ldc-,jxm-,fkpl-,fh=3,vjxk=9,dzc=1,dgt=4,hq=6,kd=5,grl-,mv=9,bq-,frd-,ngt-,tvs=8,ssjx-,tdfvs=7,jd=2,cqjzm-,rcdg=5,drhg-,ngt=9,plx-,stx-,lvv=2,pnj-,srv-,sc=2,mrn-,lmcbt-,pcr=8,cmk=4,trp=5,vkpgz=5,ngt-,ggk=9,ccfg=6,vlbzt=9,lz-,pcr-,lf=5,jgnm-,gxg=4,vqbmds=8,pdnmg-,cx=6,gjl=9,xcd-,vnzlsj-,znlg-,kff=8,cfj-,tzx-,vx-,fq-,ld-,qmgfxs=1,jdv-,lblcs=5,rsxcb=5,dk-,qqj-,znlg-,czx-,xq-,nmj-,dstpv=8,mtskb=8,hl=1,lt-,jc-,ntbsn-,jtlk-,qc=8,znnhs-,hshl-,gvt=7,dz-,fm-,zfbl-,nbmh=8,gcz=9,gv-,vjzqb-,mqv=8,dcdj=7,hfz-,ggc=3,sv-,mxmmk=9,pxfmfv=1,vq-,lmcbt-,khk=8,dk=1,kpv-,dkk-,hfqtc-,lrh=5,mkq-,zr=9,chkn=6,jvv-,sv-,hqfmx-,sthr=1,cmgtn=8,qp-,bqn-,dv=8,kzv-,mrn-,zn=7,lx=5,vzh=8,cjlm=9,bqn-,cs=7,ssn-,kz=4,dmxqf-,lk=1,kjr=7,rj=3,tpmkq=6,qrjvc=9,nglp-,jtlk=2,bzqqc-,mtr=4,dprthp-,jxm=6,vn=6,zh=5,blh-,fprt=1,jvl-,kqc=1,sthr-,cjv-,nr-,fs-,pft=7,lxl-,rqkqq=6,srf-,vcp-,lhljjx-,jcv=9,zjmhlp-,chv=6,kdn=1,tpx=5,ndm-,lqvnj=3,rv-,nsvq-,zkvc=5,nx=3,ggk=8,vrrdf-,pcvhq=3,grb-,nnh=8,fprt-,grp-,cf-,tdthvb-,gqpr=7,dp=9,mk-,qsv=3,cmgtn-,pc-,qvc-,xzh=2,jxm-,bfx-,ssn=5,bhmp-,pr-,tzx=5,brx=3,jc=6,dgt=8,pbmq-,br=5,xbjb=4,mv-,chm-,lm-,qmgfxs-,lblcs=5,dk-,ltpp-,qqv=8,ghm=7,qmkzs=8,hvxbfz-,cs-,pl=2,pjt=6,th=3,mj=6,bzqqc=1,ntbsn-,cjlm-,kjr-,lj=6,nnh-,qshv=7,vg=5,rpl=8,kqjd=7,lk-,ltpp=1,dk-,ldc=7,tz=5,hl-,mqv-,dpx=9,xbs=9,pdnmg-,jxm-,qnt-,qgjvgz=3,qc=1,brx=1,dkz-,qrjvc-,bc=2,hcz=1,chkn=2,zr-,psq-,tm-,dbkc-,nlm-,gvt-,np=6,vcp-,qq=9,ns=2,cv=3,vnz-,zsj=9,chcgr-,mjcl=9,sn-,sc-,mrn-,bj-,cb=1,qn=6,fj-,cb=4,klcz-,qbk-,pnh-,zc=5,kjq=8,pmkh-,xcv-,mv=6,fmk-,zkvc=6,nzn=3,rmb=4,tpmkq=7,hfqtc=1,hshl=8,xlh-,qn-,zsh-,pl-,qg=1,fbt-,dbms-,tl=5,hkr=7,jslp=8,rp=4,tgk=8,vc-,pmcpr-,cfj=9,vkpgz=1,vr=2,ckdl=4,dfr-,sfzcz=4,sthr-,ld=9,bhmp=9,fpcls=7,hrr-,clzn=9,bx=4,br=8,kcv=2,hh=4,hhj-,tdthvb=8,fn=9,rqkqq=7,hcz=4,fm-,qn=5,htxd-,bx=8,xkt=5,kff=1,cx=6,fn=1,kd-,chv=5,tjz-,cd=6,pqk=8,mf=3,dpx=8,bvc=2,cx-,cmk-,kll-,vjm=1,gjl-,fhvt=8,tjz-,xg=4,ssn=3,jvv=1,cpx-,hsstf=1,pmcpr-,stx=8,mxq-,lll=3,lrh-,qd-,clzn=6,nf-,fvhz=8,hspb=4,vc-,vnz=4,qshv-,xbjb=3,ghm=9,gvv=4,nsvq=3,bd=2,nt-,thm-,xbb-,tp-,bl-,brj=7,grp=8,cxmkv-,bd-,bgnt-,lmcbt=7,fmnz-,gpq-,fjp=1,mqv-,htxd=4,rj-,qg=2,cs-,jdfnb=7,dbms=6,lt=2,pr-,rcdg-,ml-,dpx-,lvv-,tr-,prrp=3,bfx-,mptk-,htxd-,grp-,lm=9,nhvt-,vnz-,nm-,pnj-,ndm=7,hmjg-,zqj-,kd=3,znlg-,ztqq=5,cbx=9,kzv=3,xc=5,dprthp-,qc=1,kqjd=6,grl-,hrpd-,td-,vg=4,lj-,hq-,grb=3,gl-,pcm=2,nhvt=1,dj=8,dkz=6,hr=5,fj-,cmgtn-,kxj=7,bj=2,gbr=7,pv=1,vmtr-,vjzqb-,khk=9,bnvn=5,ffgvvh=6,drhg=7,kqjd=2,dpx-,bq=9,dmxqf=4,qx-,fhvt-,klfhc-,dkk-,zpk=1,hhhbhd-,vltf-,ggk=3,kzv-,sjx=9,lk-,lfr-,qtlz-,hr=7,st-,ld-,bhmp=8,cbx-,cjlm=2,jdv=2,bb=8,nglp=4,xbjb-,dvr=4,chkn=3,dpjtlc=2,pnh-,tz=8,mcs-,nglp=5,ccfg=3,vjzqb-,bmqz=1,qnr=2,kjr-,lx-,nngd=9,xbjb-,sdznb-,pdnmg=5,jr-,sgs-,jc=9,qx=8,jd-,vqt-,bxs-,gk-,qn=7,bx=5,nzq=1,mxq=8,tts=1,rpl-,cfj-,gnxk-,mhnmg=9,zjmhlp-,jd=7,cct=2,dstpv-,vjm-,sgs-,hl=7,tgk=3,xbb=1,ffgvvh-,frp-,bx-,dj=6,cvk=9,ssn-,hspb=9,bp-,cpx-,qsbn-,cjlm=4,mqv-,hr=3,vpjk-,tjz-,rj=4,jxsq=3,hh-,vnz=6,qqv=4,ns-,gxg=7,hfqtc-,chcgr-,cj=6,tdthvb=7,rzrm=4,mhnmg-,cxmkv-,gk=8,rcdg-,hhj-,xn=5,gkhk=4,tnxq-,rpl-,hsstf=7,dpjtlc=8,ltpp-,kr=4,gqpr=9,cvslb=4,nnh=4,lt-,nk=5,pcvhq-,tts-,sndj-,vdn=9,qd-,kr-,ldc-,jk-,kjq-,zqj-,rj-,mg=5,hq=3,cjlm-,hb-,jfv=7,tl-,jxsq-,ccfg=4,pc-,vfc-,vmtr-,qbk-,nsvq-,bksx-,mjl=5,xlh-,hk=4,rp=7,tb-,xzq=2,tqzl=4,nr=8,bzkz-,xmqr-,pjt=5,bj-,qqv-,zpdm=1,pm=7,bfx-,kcgvv-,rmb-,kpv=6,nt-,xcd-,tvs-,tj=8,pcvhq=4,djxm=5,bhmp=2,cvk=3,cb=8,cct-,grp-,qz-,nmj=1,psq-,jmqcnd-,mkq-,gt=1,qx-,lfr-,lj=7,sstzdv-,mmq=9,hh-,vnzlsj=7,gvv-,brx-,gbr=1,bq=6,hfz=3,gc=5,spqgbb=3,fbt-,td-,ld=3,gkhk-,klcz=9,pr=3,bxs-,bhn-,lpl-,czx-,cct=6,rc-,lfr=3,vg=1,ltcr=6,pdnmg-,cdbp=7,kcc=9,xcd-,xcd=9,hmjg=6,gkr=7,qjfj-,vcp=6,ndn=3,tdfvs-,hr-,xmqr-,bhmp-,mq=1,cjv=4,spq-,bzqqc-,zpdm-,dbkc-,cd=2,gdnmgb-,kf-,jr-,lt-,ttp-,ldc=8,csb=1,pnj=3,mk-,jl=9,bdds-,jgnm=9,fbt-,pm=4,fh-,kcgvv-,bmqz-,nglp=9,ccfg=4,nbmh-,zd=3,mkq-,fhvt=5,nmn-,grp=6,vm-,rsxcb-,hfqtc=5,mcs-,rsn=1,pn=5,mcs=9,cs=8,mcs-,vq=3,gt=8,nt-,gkhk=1,ccfg=6,jslp=6,rqkqq=4,chv-,llnfd-,zjmhlp-,vg-,frd=5,zpgzv=1,nt=4,pjvc-,tjz=8,ddsg=8,qnt-,dvr-,jvv=8,qk-,np-,ml=1,pxfmfv-,hb=4,cx-,mmq=4,nfrn=8,czncl-,ckdl-,dkk=2,kcv-,cb=5,mtc-,cmk=8,jmqcnd=1,rqkqq-,dz-,cs-,mnm=1,mh-,kp-,ssxq-,tbh-,pdnmg=8,vq=2,zsb=3,xcd-,jbd=9,hbl=9,chv=9,qr=9,clzn-,sc-,gbr=5,rpl-,dcdj=7,jslp=4,bmqz=3,cgc=3,glv-,bxs=5,nbmh-,mv-,td=2,pcr-,pf=1,qkf=3,psq=5,kff-,ngt-,ffgvvh-,llnfd=6,tts=6,rv=3,ggc-,llnfd=4,tbh=5,rqkqq=5,vnrz=7,qd-,zb=6,nz=2,mjl=7,bnvn=3,bfx-,zjmhlp=3,ndm-,cct-,dpx=5,mptk-,sc-,fm=7,zkvc=3,ndn=5,lg=6,qtlz-,fcmk-,qd=8,pdls-,cqjzm-,hhj-,dzc-,vpjk-,kqc-,zsj=5,jc-,vbn-,ll=2,kjq-,cfj-,qd=2,mj-,nglp=7,csb=2,tv=3,dmxqf=2,vnzlsj-,vqt-,nj-,ljczkh-,pbmq=4,spqgbb=9,lpl-,vjxk-,qsv-,vpjk-,csb=9,vmtr-,vxc=2,bksx-,pjqc=4,tv-,sfzcz-,mqnc-,lx=7,sstzdv-,tv-,ntbsn=7,tz-,khk-,np-,tl-,jl-,brx-,tj=9,pnh-,nk=2,ldphj=7,mtc-,pdnmg=2,qr=7,llnfd-,xbjb=9,fbt=7,jkmf=2,jxm-,xg=8,ccfg=1,rpl-,fpn-,cqjzm-,gxg-,dbkc=2,jhq=7,cjlm-,bq-,fs-,gqpr-,pdnmg-,pcm-,znnhs-,nngd-,nzn=7,vl-,brx-,qq-,sc=3,gvv-,rmb=9,xvp=3,tl=5,ckdl-,rcdg-,dkz-,nlm-,dcdj=5,dv-,vxc=6,rcdg=3,ttp-,cjv-,dcdj=3,cfj=6,qsbn=8,cct=8,jxm=9,vjm=7,fprt-,mf=1,ss-,zsx-,gv-,pft-,glv-,ghk-,ckdl=6,qg-,fjkx=2,zf=9,bx-,zsb=4,jgnm=4,nr-,rs-,gl=2,sr=6,hfz=7,mtr-,qz-,nglp=3,gqpr=3,ppt=1,pmcpr-,nsvq=6,qrjvc-,rzrm-,rh=2,qshv=4,ll-,xj=5,bc-,vltf=6,ztqq=3,srv-,pmkh-,xlh-,pdls=8,kqjd-,gqpr-,cx-,bqn=3,lll=2,pcr-,lpl=6,cgq=5,rsxcb-,qrjvc-,bp-,kjr-,sthr-,qz-,vm=2
"""
]


if __name__ == "__main__":
    main()

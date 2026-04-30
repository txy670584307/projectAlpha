---
name: "java-po-dict-generator"
description: "Generates Excel data dictionaries from Java PO files in any specified folder with intelligent field name translation. Invoke when user needs to create database documentation from JPA entity classes or asks for PO file analysis."
---

# Java PO文件数据字典生成器

这个技能帮助你从Java PO（Persistent Object）文件自动生成Excel格式的数据字典。

## 功能概述

该技能可以：
- 自动扫描指定文件夹下所有PO文件（以"PO.java"结尾）
- 解析JPA注解（@Entity, @Table, @Column, @Id等）
- 提取字段信息：字段名、中文名称、列名、数据类型、主键标识、备注、是否必填
- **智能字段名翻译**：自动理解字段名并翻译成适合的中文
- **优化的列顺序**：字段名放在第一列，中文名称放在第二列
- 智能转换Java数据类型为Oracle数据类型
- 生成Excel文件，每个PO文件对应一个工作表（Sheet）
- 自动添加边框和调整列宽
- **支持任意文件夹**：可以指定任意文件夹名称，或自动扫描所有包含PO文件的文件夹
- **灵活的输出**：按照文件夹名称生成对应的Excel文件

## 何时使用

当用户遇到以下情况时，应该调用此技能：
1. 需要从Java PO文件生成数据库文档
2. 需要分析JPA实体类的字段信息
3. 需要创建数据字典或数据库表结构文档
4. 需要将PO文件转换为Excel格式的数据字典
5. 用户询问"如何生成数据字典"或"如何分析PO文件"
6. 用户需要处理任意指定的文件夹，而不是固定的decl/ship目录

## 完整脚本代码

将以下代码保存为 `generate_po_dictionaries.py` 文件：

```python
import re
import os
import pandas as pd
from pathlib import Path
from openpyxl.styles import Border, Side

def parse_po_file(file_path):
    """解析PO文件，提取表名和字段信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取表名
    table_match = re.search(r'@Table\s*\(\s*name\s*=\s*["\']([^"\']+)["\']', content)
    table_name = table_match.group(1) if table_match else os.path.basename(file_path).replace('PO.java', '')
    
    # 提取字段信息
    fields = []
    
    # 改进的解析方法：使用更强大的正则表达式匹配 @Column 注解
    column_pattern = r'@Column\s*\((?:[^()]|\([^()]*\))*\)'
    
    for match in re.finditer(column_pattern, content):
        column_text = match.group(0)
        
        # 提取name属性
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', column_text)
        if not name_match:
            continue
        column_name = name_match.group(1)
        
        # 提取nullable属性
        nullable_match = re.search(r'nullable\s*=\s*(true|false)', column_text)
        nullable = nullable_match.group(1) if nullable_match else "true"
        
        # 提取length属性
        length_match = re.search(r'length\s*=\s*(\d+)', column_text)
        length = length_match.group(1) if length_match else None
        
        # 查找对应的private字段（在@Column之后）
        after_column = content[match.end():]
        field_pattern = r'\s*private\s+(\w+)\s+(\w+)\s*;'
        field_match = re.search(field_pattern, after_column)
        
        if not field_match:
            continue
        
        java_type = field_match.group(1)
        field_name = field_match.group(2)
        
        # 转换数据类型
        data_type = convert_data_type(java_type, length)
        
        # 确定是否必填
        is_required = "必填" if nullable == "false" else ""
        
        # 检查是否是主键
        is_primary = False
        # 检查@Column前面最近的注解是否有@Id
        before_column = content[:match.start()]
        # 找到最近的@Id注解（在当前@Column之前）
        id_pattern = r'@Id[^\n]*\n'
        id_matches = list(re.finditer(id_pattern, before_column))
        if id_matches:
            # 找到最近的@Id注解
            last_id_match = id_matches[-1]
            # 检查@Id和@Column之间是否有其他字段定义
            between = before_column[last_id_match.end():]
            if not re.search(r'private\s+\w+\s+\w+\s*;', between):
                is_primary = True
        
        # 提取字段注释中的中文名称
        chinese_name = extract_chinese_name_from_comment(before_column)
        
        # 如果注释中没有中文名称，则使用智能翻译
        if not chinese_name:
            chinese_name = generate_chinese_name(field_name)
        
        # 生成PK/INDEX和备注
        pk_index = ""
        remark = ""
        if is_primary:
            pk_index = "pk"
            # 检查是否有序列生成器
            seq_match = re.search(r'@SequenceGenerator\s*\(\s*name\s*=\s*["\'][^"\']+["\'].*?sequenceName\s*=\s*["\']([^"\']+)["\']', content)
            if seq_match:
                remark = f"对应{seq_match.group(1)}"
        
        fields.append({
            "column": column_name,
            "field_name": field_name,
            "chinese_name": chinese_name,
            "data_type": data_type,
            "pk_index": pk_index,
            "remark": remark,
            "is_required": is_required
        })
    
    return table_name, fields

def convert_data_type(java_type, length):
    """转换Java数据类型为Oracle数据类型"""
    if java_type == "Long":
        if length:
            return f"NUMBER({length})"
        return "NUMBER(16)"
    elif java_type == "Integer":
        if length:
            return f"NUMBER({length})"
        return "NUMBER(10)"
    elif java_type == "String":
        if length:
            return f"VARCHAR2({length} char)"
        else:
            return "VARCHAR2(255 char)"
    elif java_type == "Double":
        if length:
            return f"NUMBER({length})"
        return "NUMBER(10,2)"
    elif java_type == "Float":
        if length:
            return f"NUMBER({length})"
        return "NUMBER(10,2)"
    elif java_type == "Date":
        return "DATE"
    else:
        return java_type

def extract_chinese_name_from_comment(before_field):
    """从字段注释中提取中文名称"""
    # 查找字段定义前面的注释
    # 匹配 //开头的注释，提取其中的中文内容
    comment_pattern = r'//\s*([^\n]+)'
    comment_matches = list(re.finditer(comment_pattern, before_field))
    
    if not comment_matches:
        return None
    
    # 获取最后一个注释（最接近字段定义的注释）
    last_comment = comment_matches[-1].group(1).strip()
    
    # 检查注释中是否包含中文
    if not re.search(r'[\u4e00-\u9fff]', last_comment):
        return None
    
    # 清理注释，移除额外的说明信息
    # 例如： "//过境类型	参数库选择（如果是外贸，此表中没有码头过境，如果是内贸，有码头过境） 16=港口过境  17=码头过境"
    # 只保留前面的中文名称部分
    cleaned_comment = re.split(r'[\t\s]+', last_comment)[0].strip()
    
    return cleaned_comment if cleaned_comment else None

def generate_chinese_name(field_name):
    """根据字段名生成中文名称，智能理解并翻译"""
    # 常见字段映射 - 基于危防业务危险品申报公用表数据字典
    mapping = {
        "acceListId": "附件清单序号",
        "acceListNo": "附件清单序号",
        "acceptanceResult": "回执结果",
        "acceptance_result": "回执结果",
        "accidentDesc": "意外情况说明",
        "accidentID": "事故代码",
        "accidentId": "事故代码",
        "accpNo": "受理回执号",
        "acidity": "酸度",
        "ackCheckListId": "附件记录序号",
        "ackContent": "回执内容",
        "ackErrId": "回执附带错误序号",
        "ackId": "回执序号",
        "ackNo": "受理\审核回执号",
        "ackType": "回执类型，4错误回执",
        "ack_no": "序号",
        "actSeagauge": "实际吃水（米）",
        "actTonnage": "实际载重吨(吨)",
        "actionTime": "抵/离港时间",
        "actived": "是否有效",
        "addiDate": "加入的添加剂日期(YYYY-MM-DD)",
        "addiExpirDate": "添加剂有效使用期(YYYY-MM-DD)",
        "addiList": "包件",
        "addiName": "添加剂名称",
        "addiNo": "物品添加剂证明编号",
        "addiNum": "加入的添加剂数量及单位，标明计量单位",
        "addi_date": "添加剂日期",
        "addi_expir_date": "添加剂过期日期",
        "addi_name": "添加剂名称",
        "addi_num": "添加剂编号",
        "additionalInfo": "附加信息",
        "additional_info": "附加信息",
        "additiveWashing": "使用清洁剂/添加剂洗(是/否)",
        "addr": "联系地址",
        "addrCN": "中文联系地址",
        "addrCn": "中文联系地址",
        "addrEN": "英文联系地址",
        "addrEn": "英文联系地址",
        "addr_cn": "中文联系地址",
        "addr_en": "英文联系地址",
        "address": "联系地址",
        "agencyCode": "船舶代理EDI编号",
        "agencyEDICode": "代理EDI编码",
        "agencyEdiCode": "船代EDI编号",
        "agencyName": "船舶代理名称",
        "agencyNameCN": "订舱单位中文名",
        "agencyNameCn": "订舱单位中文名",
        "agencyNameEN": "订舱单位代码",
        "agencyNameEn": "订舱单位英文名",
        "agency_code": "船舶代理EDI编号",
        "agency_name": "船舶代理名称",
        "aliasName": "液态危险品别名",
        "angleOfRepose": "静止角",
        "aplID": "船申报报文号",
        "aplId": "业务申请编号，对应CargoApplyInfo的AplId",
        "apl_id": "货申报报文号",
        "aplid": "申报业务编号",
        "arrivedTime": "抵港时间 C/M",
        "audtNo": "审核回执号",
        "bERTH": "作业地点代码",
        "bOAT_FLAG": "海船/内河船标识",
        "bargePort": "驳运港",
        "bayNo": "贝位",
        "berth": "停靠码头代码",
        "berthApplyInfo": "靠泊申请信息",
        "berthFirst": "横向位置",
        "berthSecond": "纵向位置",
        "berthStatus": "舱室状态",
        "berthThird": "垂直位置",
        "berth_apply_info": "靠泊申请信息",
        "bigDataId": "上传返回序号",
        "bigDataTime": "大数据报文建立时间",
        "big_data_id": "上传返回序号",
        "big_data_time": "大数据报文建立时间",
        "bigdataId": "报文上传序号",
        "bilgeWater": "压载/污水舱类型",
        "bilge_water": "舱底水",
        "billId": "提单序号",
        "billInfo": "提单信息",
        "billNo": "提单号",
        "bill_info": "提单信息",
        "boatFlag": "海船/内河船标识",
        "boat_flag": "海船/内河船标识",
        "boilingPoint": "沸点",
        "bookAgencyCode": "订舱单位编号",
        "bookAgencycode": "订舱单位代码",
        "buildDate": "建造日期(CCYYMM)",
        "build_date": "建造日期(yyyy-MM-dd)",
        "bulkCtnReg": "中型散装容器规定",
        "bulkCtnWiz": "中型散装容器导则",
        "bulk_ctn_reg": "中型散装容器规定",
        "bulk_ctn_wiz": "中型散装容器导则",
        "burnDown": "可燃下限",
        "burnUp": "可燃上限",
        "businessType": "业务类型",
        "business_type": "业务类型",
        "cALL_CODE": "挂靠港代码",
        "cALL_PORT": "挂靠港",
        "cALL_PORT_CODE": "挂靠港代码",
        "cARR_CODE": "承运人",
        "cTypeCabin": "C型独立液货舱",
        "cabinConditionCtrl": "货舱环境控制",
        "cabinVentilate": "液货舱透气情况",
        "callCode": "下一港代码",
        "callPort": "上一港名称",
        "call_code": "下一港代码",
        "call_port": "上一港名称",
        "cancelFlag": "撤销标记",
        "capacity": "每一容器容量",
        "cargoAplID": "货申报报文号",
        "cargoAplId": "货申报报文号",
        "cargoAudtNo": "审核回执号",
        "cargoChanged": "货申报是否修改过",
        "cargoDirect": "货物流向标志",
        "cargoDirection": "需要特殊附件提示的运输方式",
        "cargoFileDesc": "货代描述信息",
        "cargoGroup": "货物组别",
        "cargoID": "液态危险品编号",
        "cargoId": "液态危险品编号",
        "cargoInfo": "货物信息",
        "cargoOwner": "货主名称",
        "cargoProp": "货物特性",
        "cargoReactivity": "货物反应性",
        "cargoSendTime": "货代发送时间",
        "cargoType": "货物种类 粘性非粘性散货",
        "cargo_info": "货物信息",
        "cargo_owner": "货主",
        "cargo_owner_code": "货主代码",
        "cargo_prop": "货物特性",
        "cargoowner": "货主",
        "cargoownerCode": "货主备案代码",
        "cargotaskId": "过境序号",
        "cargotask_id": "货物任务ID",
        "carrCode": "承运人代码",
        "carr_code": "承运人代码",
        "caseNo": "箱号",
        "certAmount": "总量",
        "certId": "附加编号（附件名称）",
        "certListNo": "附件清单序号",
        "certMemo": "备注",
        "certName": "附件名称",
        "certNo": "附件编号",
        "certType": "证件类别",
        "certValidDate": "附件有效期",
        "cert_id": "附件序号",
        "cert_no": "装箱证明书编号",
        "cert_type": "附件类别",
        "checkFlag": "查验标记",
        "checkflag": "查验标记",
        "chemicalCabinType": "散化舱型",
        "chemicalGasSteamDetect": "蒸汽探测(散装化学品)",
        "chemicalTankType": "化学品船船型",
        "chemical_tank_type": "化学品船船型",
        "cleanedFlag": "空的但未清洁",
        "clearBerthAplId": "洗舱序号",
        "clearBerthApplyInfo": "清除靠泊申请信息",
        "clearTankMode": "洗舱方式",
        "clear_berth_apply_info": "清除靠泊申请信息",
        "clientFunction": "客户端功能",
        "client_function": "海事下发的权限",
        "columnHINT": "提示信息",
        "columnHint": "提示信息",
        "columnName": "提示信息",
        "company": "生产厂家",
        "companyAddressTel": "船舶经营人联系地址/电话",
        "companyCode": "公司代码",
        "companyName": "公司名称",
        "companyWeb": "公司网址",
        "company_address_tel": "公司地址电话",
        "conVoyFlag": "强制护航",
        "connectingVesselId": "一/二程船IMO编号或者船舶初始登记号",
        "connectingVesselName": "一/二程船船名",
        "connectingVesselVoyage": "一/二程船航次",
        "connector": "联系人",
        "contactAddrCN": "中文联系地址",
        "contactAddrEN": "英文联系地址",
        "contactNameCN": "中文名称",
        "contactNameEN": "英文名称",
        "contactPerson": "联系人",
        "contactTelNo": "联系电话",
        "contactZipNo": "邮编",
        "contact_person": "联系人",
        "containCert": "装箱证明书",
        "containDate": "预定装箱日期(CCYYMMDD)",
        "containNo": "集装箱箱号(无用)",
        "contentWeight": "容器内装净重",
        "controlTempe": "控制温度",
        "convoyFlag": "是否强制护航",
        "copNo": "企业编号",
        "cop_no": "企业编号",
        "country": "国家",
        "countryCode": "国家代码",
        "countryNameCN": "国家中文名称",
        "countryNameEN": "国家英文名称",
        "createDate": "记录生成时间",
        "createOp": "创建人",
        "createTime": "创建时间",
        "create_op": "创建人",
        "create_time": "创建时间",
        "ctnGrossWeight": "箱毛重（组件毛重）",
        "ctnNetWeight": "箱内货物净重（组件内货物重量）",
        "ctnPackage": "箱内件数",
        "ctnStatus": "拼箱状态",
        "ctngrossWeight": "车辆毛重",
        "ctngrossweight": "箱毛重",
        "ctnnetWeight": "车辆内货物净重",
        "ctnnetweight": "组件内货物重量",
        "ctypeCabin": "C型独立液货舱",
        "deClareType": "申报类型",
        "declarationId": "装箱申明书编号",
        "declareType": "申报类型",
        "defaultFlag": "是否默认",
        "default_flag": "是否默认",
        "deleteFlag": "删除标记",
        "delivery": "交货地",
        "deliveryId": "交货地代码",
        "deliveryPortCode": "交货地代码",
        "deliveryPortName": "交货地名称",
        "density": "散货密度",
        "departOfCert": "签发机构",
        "desc": "描述信息",
        "descr": "描述信息",
        "descri": "描述信息",
        "description": "描述",
        "docCheckFlag": "正本核查标记",
        "docFilename": "文件名",
        "dockDesc": "码头全称",
        "dockInfo": "靠泊信息",
        "dockName": "码头简称",
        "dock_desc": "码头全称",
        "dock_info": "靠泊信息",
        "dock_name": "码头简称",
        "done": "刚入库回执的标志",
        "downLoadFlag": "是否下载",
        "drainageDestination": "污水排放去向",
        "drainagePlaceCode": "污水作业码头",
        "drainageQuantity": "预计排放污水/混合物",
        "eDICode": "EDI代码",
        "eDIId": "用户的EDI编号",
        "eDINo": "货申报申报单位EDI代码编号",
        "eMSFlag": "应急状态",
        "eMSNo": "航运危险品应急措施号",
        "eMSStep": "航行时间超过添加剂有效期时，应采取的措施",
        "eRRAckId": "错误回执序号",
        "eRRNo": "错误序号",
        "eSTI_SAIL": "预计离港日期",
        "ediCode": "订舱单位EDI编码",
        "ediId": "码头EDI代码",
        "edi_code": "edi代码",
        "edi_id": "码头EDI代码",
        "electricity": "导电率",
        "electricityRate": "导电率",
        "email": "邮箱",
        "emergency": "紧急通讯录",
        "emergencyEquipment": "应急设备",
        "emgContact": "紧急通讯录",
        "emgTempe": "应急温度",
        "emsNo": "应急措施",
        "emsStep": "航行时间超过添加剂有效期时，应采取的措施",
        "ems_no": "应急措施",
        "emsstep": "EMS步骤",
        "encloseOperCode": "围油栏作业队伍备案代码",
        "encloseOrCustody": "需要落实围油栏防控措施",
        "endOperTime": "预计结束作业时间",
        "entOrder": "查询条件顺序",
        "ent_order": "查询条件顺序",
        "enterpriseIp": "企业ip",
        "enterpriseName": "企业名称",
        "enterprisePassword": "企业密码",
        "enterpriseState": "企业状态",
        "enterprise_ip": "企业ip",
        "enterprise_name": "企业名称",
        "enterprise_password": "企业密码",
        "enterprise_state": "企业状态",
        "equipmentClass": "电子设备分类",
        "equipmentFlashPoint": "电子设备闪点",
        "equipmentTempLevel": "电子设备温度等级",
        "errCode": "出错代码信息",
        "errContent": "错误记录描述",
        "errDesc": "错误描述",
        "errId": "错误编号",
        "errName": "错误信息",
        "errType": "错误代码类型",
        "errfields": "出错字段号",
        "errno": "出错记录号",
        "errorCode": "错误代码",
        "errorDesc": "原因描述",
        "errorFieldsNo": "错误字段号",
        "errorRecordNo": "错误记录号",
        "error_code": "错误代码",
        "error_desc": "原因描述",
        "error_fields_no": "错误字段号",
        "error_record_no": "错误记录号",
        "espTechReq": "特殊技术要求",
        "estiSail": "抵/离港日期",
        "esti_sail": "抵/离港日期",
        "expirationTime": "过期时间",
        "expiration_time": "过期时间",
        "farFood": "远离食品",
        "farHotSource": "远离热源",
        "farLivingArea": "远离生活区",
        "far_food": "远离食品",
        "far_hot_source": "远离热源",
        "far_living_area": "远离生活区",
        "fax": "传真",
        "fieldCode": "字段code",
        "fieldName": "字段中文名称",
        "fieldOrder": "显示顺序",
        "field_code": "字段code",
        "field_name": "字段中文名称",
        "field_order": "显示顺序",
        "fileDesc": "发送报文的文件描述",
        "fileDescription": "文件说明",
        "fileFunction": "文件功能",
        "fileShipDesc": "发送船代的文件描述",
        "file_description": "文件说明",
        "file_function": "文件功能",
        "fireExti": "灭火剂",
        "fire_exti": "灭火剂",
        "fireproofing": "防火",
        "firstInspectDate": "首次检验日期(CCYYMMDD)",
        "flammabilityTemperature": "自燃温度",
        "flashPoint": "闪点",
        "flash_point": "闪点",
        "forgiveCargo": "换装物质名称",
        "forgiveMode": "免除预洗方式",
        "formula": "分子式",
        "gCargoDirection": "过境类型",
        "gCargoWeight": "货物重量",
        "gCargoownerCode": "货主代码",
        "gLoadPortCode": "装货港代码",
        "gLoadPortName": "装货港名称",
        "gShippingNameCN": "正确运输名称（中文）",
        "gShippingNameEN": "正确运输名称（英文）",
        "gShippingNameSYS": "正确运输名称(中文)",
        "gTankFirst": "横向位置",
        "gTankId": "过境舱室序号",
        "gTankSecond": "纵向位置",
        "gTankThird": "垂直位置",
        "gTradeFlag": "内外贸标志",
        "gUnloadPortCode": "卸货港代码",
        "gUnloadPortName": "卸货港名称",
        "gasCabinSteamCtrl": "液货舱内蒸汽空间的控制",
        "gasFreeing": "驱气作业(是/否)",
        "gasProperty": "散装液化气性质",
        "gasSteamDetect": "蒸汽探测(液化气)",
        "gasTankType": "液化气船船型",
        "gas_tank_type": "液化气船船型",
        "grossWeight": "每一包件毛重",
        "gross_weight": "每一包件毛重",
        "guideClear": "指南-清扫",
        "guideEmergency": "指南-应急",
        "guideLoad": "指南-装卸货物要求",
        "guideProtect": "指南-防护",
        "guideTrans": "指南-装运货物要求",
        "guideTransport": "指南-装卸货物要求",
        "guideUnload": "指南-装卸货物要求",
        "guideWeather": "指南-天气",
        "hODUnit": "油类密度单位",
        "handCode": "检查表表头||条件名称code",
        "hand_code": "检查表表头||条件名称code",
        "handlingTemp": "装卸货物温度",
        "harm": "危害性",
        "hasParticleSize": "颗粒尺寸是否适用",
        "havingCert": "是否含有货物对应的证书",
        "hazardClass": "主危险类别",
        "hazard_class": "主危险类别",
        "headName": "检查表表头||条件名称",
        "headOrder": "显示顺序",
        "head_name": "检查表表头||条件名称",
        "head_order": "显示顺序",
        "heavyoilDensity": "油类密度(15°C)",
        "heavyoilVisCosity": "油类粘度(50°C)",
        "highFlammability": "可燃上限",
        "hintMessage": "特殊附件提示内容",
        "hisImoNo": "卸载船IMO编号",
        "hisShipCompany": "船舶经营人",
        "hisShipLine": "航线性质",
        "hisShipNameCN": "卸载船中文船名",
        "hisShipNameEN": "卸载船英文船名",
        "hisShipRegister": "卸载船初始登记号",
        "hisVesselCall": "卸载船呼号",
        "hisVoyage": "卸载船航次",
        "historyID": "历史序号",
        "historyId": "卸载船历史序号",
        "homePosi": "标识表&字段",
        "home_posi": "标识表&字段",
        "iMONo": "装卸载船IMO编号",
        "iMO_NO": "IMO编号",
        "id": "编号",
        "imoNo": "IMO编号",
        "imo_no": "IMO编号",
        "inEffectFlag": "有效标记",
        "inOutFlag": "船舶进出港标记",
        "inceptCompanyCode": "拟送接收单位",
        "infectantKind": "化学品污染类别",
        "inspectorId": "装箱检查员编号",
        "isDefault": "是否默认",
        "jarWinReg": "罐柜导则规定",
        "jarWinUn": "罐柜导则UN",
        "jarWizImo": "罐柜导则IMO",
        "jarWizReg": "罐柜导则规定",
        "jarWizUn": "罐柜导则UN",
        "jar_win_reg": "罐柜导则规定",
        "jar_win_un": "罐柜导则UN",
        "jobNo": "企业管理编号",
        "jobno": "企业管理编号",
        "lC": "口服",
        "lD": "皮触",
        "lDUnit": "液体相对密度单位",
        "lastPortCode": "危险品最后装货港代码",
        "lastPortName": "危险品最后装货港名称",
        "lastUpdTime": "最近更新时间",
        "leadFlag": "是否是数据收发货申报接收",
        "licensePlateNumber": "车牌号",
        "lighteragePort": "港内驳运目的地",
        "lighterageport": "港内驳运目的地",
        "lighteringOperator": "过驳经营人",
        "limitFlag": "限量",
        "limited": "限 量",
        "linerType": "班轮类型",
        "liquidAcceListInfo": "液体货物清单信息",
        "liquidDensity": "液体相对密度",
        "liquidDensityUnit": "液体相对密度单位",
        "liquidPressure": "液化压力",
        "liquidTemperature": "液化温度",
        "liquid_acce_list_info": "液体货物清单信息",
        "loadDate": "预定装船日期(CCYYMMDD)",
        "loadPort": "装货港口名称",
        "loadPortCode": "装货港代码",
        "loadPortId": "装货港口代码",
        "loadPortName": "装货港名称",
        "loadVesselType": "装/卸载船标志",
        "load_port": "装货港",
        "locationOfStorage": "积载位置",
        "locationOfStorageId": "积载位置序号",
        "lockFlag": "锁定标记",
        "loginId": "登录名",
        "loginName": "姓名",
        "login_id": "登录名",
        "login_name": "姓名",
        "lowFlammability": "可燃下限",
        "loxkind": "散装液化气性质",
        "mFAGNo": "医疗急救指南号",
        "mail": "电子邮箱",
        "maritimeCode": "海事代码",
        "maritimeId": "码头海事编号",
        "maritime_id": "码头海事编号",
        "marksNo": "货物标记",
        "maxCancelNo": "船开后撤销最大数字",
        "medicalStep": "医疗急救指南",
        "medium": "洗舱介质",
        "memo": "备注",
        "menuAlter": "菜单ALTER",
        "menuCode": "菜单代码",
        "menuIcon": "菜单icon",
        "menuImg": "显示图片",
        "menuName": "中文描述",
        "menuNameEn": "英文名称",
        "menuOrder": "显示顺序",
        "menuUrl": "菜单URL",
        "menu_alter": "菜单ALTER",
        "menu_code": "菜单代码",
        "menu_icon": "菜单icon",
        "menu_img": "显示图片",
        "menu_name": "中文描述",
        "menu_name_en": "英文名称",
        "menu_order": "显示顺序",
        "menu_url": "菜单URL",
        "mertingPoint": "熔点",
        "messageNo": "原始报文号",
        "messageType": "回执类型",
        "message_no": "原始报文号",
        "message_type": "回执类型",
        "mfagNo": "医疗急救",
        "mfag_no": "医疗急救",
        "mfageNo": "医疗急救",
        "mfage_no": "医疗急救",
        "mobile": "座机号码",
        "modifyDate": "记录最后修改时间",
        "mpt": "海洋污染性",
        "mptFlag": "海运污染",
        "msaCode": "海事辖区代码",
        "msgSource": "信息来源",
        "msg_source": "信息来源",
        "multiPortFlag": "多码头作业标记",
        "nameCN": "中文名称",
        "nameCn": "中文名称",
        "nameEN": "英文名称",
        "nameEn": "英文名称",
        "name_cn": "中文名称",
        "name_en": "英文名称",
        "nationality": "船舶国籍代码",
        "nativeDangeNo": "国内危规编号",
        "native_dange_no": "国内危险品编号",
        "needHint": "是否需要特殊附件提示",
        "netWeight": "货物净重量",
        "nextPortCode": "下一港代码",
        "nextPortName": "下一港名称",
        "noOwnMenu": "下发权限中未拥有的菜单",
        "noOwnSys": "未拥有的申报系统",
        "no_own_menu": "下发权限中未拥有的菜单",
        "no_own_sys": "未拥有的申报系统",
        "notes": "备注",
        "oilProperty": "油类性质",
        "oilSafeStack": "内贸油轮安全结构",
        "oilTankStru": "油轮防护结构",
        "oilWashing": "原油洗舱(是/否)",
        "oil_tank_stru": "油轮防护结构",
        "oilkind": "油类性质",
        "oldPollutionCategory": "原分类体系污染类别",
        "oorRBoat": "海船/内河船标识",
        "oorrBoat": "海船/内河船标识",
        "oorr_boat": "海船/内河船标识",
        "openFlag": "集装箱状态",
        "operId": "作业序号",
        "operPlaceCode": "作业地点代码",
        "operPlaceId": "作业地点序号",
        "operReq": "经营人要求",
        "operTemperature": "作业温度",
        "oper_req": "经营人要求",
        "operationInfo": "作业信息",
        "operationOrder": "作业港序",
        "operationPlaceId": "作业地点序号",
        "operationRequirement": "特殊和操作要求",
        "operation_info": "作业信息",
        "opertionPlaceId": "作业地点编号",
        "orgAddress": "联系地址",
        "orgCancelFlag": "原始撤销标记",
        "orgCode": "公司组织机构代码",
        "orgEmail": "公司邮箱",
        "orgId": "EDI中心编号",
        "orgInEffectFlag": "原始有效标记",
        "orgLinkMan": "公司联系人",
        "orgLinkPhone": "联系电话",
        "orgName": "中文单位名称",
        "orgNameEN": "单位英文名称",
        "orgNameEn": "单位英文名称",
        "orgStatus": "原始当前状态",
        "orgType": "单位类型",
        "org_address": "联系地址",
        "org_code": "机构代码",
        "org_email": "公司邮箱",
        "org_id": "EDI中心编号",
        "org_link_man": "公司联系人",
        "org_link_phone": "联系电话",
        "org_name": "单位名称",
        "org_name_en": "单位英文名称",
        "org_type": "单位类型",
        "originalFileDesc": "原始报文,文件说明",
        "originalFileName": "原始报文,文件名",
        "originalMessageNo": "原始报文号",
        "originalSendUser": "原始报文发送人",
        "originalTime": "原始报文建立时间",
        "originalType": "原始报文,报文类型",
        "original_file_desc": "原始报文,文件说明",
        "original_file_name": "原始报文,文件名",
        "original_message_no": "原始报文号",
        "original_send_user": "原始报文发送人",
        "original_time": "原始报文建立时间",
        "original_type": "原始报文,报文类型",
        "overNo": "过驳艘次",
        "overlighterCode": "过驳作业申请号",
        "ownerAddressTel": "船舶所有人联系地址/电话",
        "owner_address_tel": "船东地址电话",
        "packageAplId": "包件序号",
        "packageClass": "包装类",
        "packageCode": "包装代码",
        "packageGrp": "包装类",
        "packageKind": "商检使用证明",
        "packageNum": "拟用包件数量",
        "packageReg": "包装规定",
        "packageTypeId": "包装类型代码",
        "packageWeight": "每个包件净重量",
        "packageWiz": "包装导则",
        "package_class": "包装类",
        "package_code": "包装代码",
        "package_reg": "包装规定",
        "package_wiz": "包装导则",
        "packingSpot": "装箱/充罐作业点",
        "packingSpotId": "装箱/罐柜作业点编号",
        "packingSpotName": "装箱/罐柜作业点名称",
        "packingSpotType": "装箱/罐柜作业点类型",
        "packing_spot_id": "装箱/罐柜作业点编号",
        "packing_spot_name": "装箱/罐柜作业点名称",
        "packing_spot_type": "装箱/罐柜作业点类型",
        "paramCode": "参数编号",
        "paramId": "参数编号",
        "paramName": "参数名称",
        "paramType": "参数类型",
        "param_code": "参数编号",
        "param_name": "参数名称",
        "param_type": "参数类型",
        "parentCode": "上级公司ORG_CODE",
        "parent_code": "上级公司ORG_CODE",
        "particleSize": "颗粒尺寸",
        "particleSizeApp": "颗粒尺寸是否适用",
        "passCargoID": "过境货物序号",
        "passExpoArea": "是否经过世博核心水域",
        "passHuangpuRiver": "是否经过黄浦江水域",
        "passingCargoInfo": "过境货物信息",
        "passing_cargo_info": "过境货物信息",
        "personId": "货主代码",
        "person_id": "人员编号",
        "personnelProtection": "人员防护",
        "phone": "联系电话",
        "pixei": "像素值",
        "pk": "主键",
        "pkCgbizapply": "ID号，主键",
        "pkCgbizapuserspot": "ID号，主键",
        "pkCgbizdangeratt": "ID号，主键",
        "pkCgbizship": "主键",
        "pkCgbizshipinfo": "主键",
        "pkCgbizunit": "ID号，主键",
        "pkCgcodbook": "ID号，主键",
        "pkCgprimarypools": "ID号，主键",
        "pkDmcodagency": "ID号，主键",
        "pkDmcodsenderreceive": "ID号，主键",
        "pollutionCategory": "新分类体系污染类别",
        "portCode": "历史港口代码",
        "portDesc": "描述信息",
        "portID": "历史港口序号",
        "portId": "港口编号或代码",
        "portInfo": "港口信息",
        "portName": "历史港口名称",
        "portNameCN": "港口名称（中文）",
        "portNameCn": "港口名称(中文)",
        "portNameEN": "港口名称（英文）",
        "portNameEn": "港口名称(英文)",
        "portReq": "港口要求",
        "port_desc": "描述信息",
        "port_id": "港口编号或代码",
        "port_info": "港口信息",
        "port_name_cn": "港口名称(中文)",
        "port_name_en": "港口名称(英文)",
        "port_req": "港口要求",
        "preAplID": "前一次申报号",
        "preAplid": "前一次申报号",
        "previousPortCode": "上一港代码",
        "previousPortName": "上一港名称",
        "privateKey": "密钥",
        "private_key": "密钥",
        "produceDate": "生产日期(YYYY-MM-DD)",
        "produce_date": "生产日期",
        "ptableType": "所属表",
        "ptable_type": "所属表",
        "publicKey": "公钥",
        "public_key": "公钥",
        "quantity": "总量",
        "rECVCODE": "报文接收方代码",
        "reactivity": "货物反应性",
        "recCode": "接收方edi代码",
        "rec_code": "接收方edi代码",
        "receiveCnName": "收货人中文名称",
        "receiveDate": "接收时间",
        "receiveEnName": "收货人英文名称",
        "receiveId": "收货人信息编号",
        "receiverDetailCN": "收货人中文信息",
        "receiverDetailEN": "收货人英文信息",
        "receiverId": "收货人信息备案代码编号",
        "recvTime": "回执接收时间",
        "recvcode": "接收方代码",
        "regDate": "备案日期",
        "regNo": "申报单位备案编号",
        "reg_date": "备案时间（yyyy-MM-dd）",
        "reg_no": "备案编号",
        "regno": "申报员备案号",
        "relativeRegNo": "收发货人备案编号",
        "remark": "备注",
        "reposeAngle": "静止角",
        "requirement": "特殊要求",
        "roleId": "角色id",
        "role_id": "角色id",
        "sHIP_AGEN": "船代EDI编号",
        "sHIP_NACODE": "船舶国籍代码",
        "sailingDateType": "航线内外贸标志",
        "saillingTime": "离港时间 M/C",
        "seaGauge": "满载吃水（米）",
        "sea_gauge": "吃水",
        "sealNo": "铅封号",
        "sealno": "铅封号",
        "sendCnName": "发货人中文名称",
        "sendCode": "发送方edi代码",
        "sendEnName": "发货人英文名称",
        "sendId": "发货人信息编号",
        "sendMaritimeDate": "发送海事局时间",
        "sendVesselDate": "发送船代时间",
        "send_code": "发送方edi代码",
        "sender": "发送方",
        "senderDetailCN": "发货人中文信息",
        "senderDetailEN": "发货人英文信息",
        "senderId": "发货人信息备案代码编号",
        "sex": "性别",
        "shipAgen": "共用舱位船公司/船代代码",
        "shipApplyInfoBusiness": "船舶申请业务信息",
        "shipCarrier": "承运人",
        "shipCarrierContact": "承运人联系方式",
        "shipCompany": "船舶经营人地址电话",
        "shipCompanyCode": "船舶经营人代码",
        "shipHistoryInfo": "船舶历史信息",
        "shipID": "船舶主键号 (企业内部的唯一标示)",
        "shipId": "企业内部的船舶标号（船舶标识号）",
        "shipInfoBusiness": "船舶业务信息",
        "shipLength": "船舶长度（米）",
        "shipLine": "航线性质",
        "shipNacode": "船舶国籍代码",
        "shipNameCN": "装卸载船中文船名",
        "shipNameCn": "中文船名",
        "shipNameEN": "装卸载船英文船名",
        "shipNameEn": "英文船名",
        "shipOwner": "船舶所有人",
        "shipQualification": "载运条件",
        "shipRegister": "装卸载船初始登记号",
        "shipWidth": "船舶宽度（米）",
        "ship_agen": "共用舱位船公司/船代代码",
        "ship_apply_info_business": "船舶申请业务信息",
        "ship_company": "船公司",
        "ship_history_info": "船舶历史信息",
        "ship_id": "船舶主键号(船舶标识号)",
        "ship_info_business": "船舶业务信息",
        "ship_length": "船长",
        "ship_line": "航线性质",
        "ship_nacode": "船舶国籍代码",
        "ship_name_cn": "中文船名",
        "ship_name_en": "英文船名",
        "ship_owner": "船东",
        "ship_register": "船舶初始登记号",
        "ship_width": "船宽",
        "shipcompany": "船舶经营人",
        "shipowner": "船舶所有人",
        "shippingNameCN": "正确运输名称(中文)",
        "shippingNameCn": "中文名称",
        "shippingNameEN": "正确运输名称(英文)",
        "shippingNameEn": "液态危险品中文名",
        "shippingNameSYS": "正确运输名称(中文)",
        "shipping_name_cn": "中文名称",
        "shipping_name_en": "英文名称",
        "shortName": "液态危险品缩写",
        "skintouch": "皮触",
        "socialCreditCode": "社会信用代码",
        "social_credit_code": "社会信用代码",
        "solubility": "水中溶解度",
        "specReq": "特殊要求",
        "spec_req": "特殊要求",
        "specialInspectDate": "特殊检验日期(CCYYMMDD)",
        "specialNature": "货物相关特殊性质",
        "specifications": "散装货物的特殊说明",
        "startOperTime": "预计开始作业时间",
        "startPortCode": "始发港代码",
        "startPortName": "始发港名称",
        "status": "回执状态",
        "stowage": "积载类",
        "stowageFactor": "积载因数 单位为(m3/t)",
        "stowageReq": "积载隔离要求",
        "stowage_req": "积载隔离要求",
        "subHazardClass": "副危险类别",
        "subHazardClass1": "副危险类别1",
        "subHazardClass2": "副危险类别2",
        "subHazardClass3": "副危险类别3",
        "subHazardClassF": "副危险类别1",
        "subHazardClassS": "副危险类别2",
        "subHazardClassT": "副危险类别3",
        "sub_hazard_class_f": "副危险类别1",
        "sub_hazard_class_s": "副危险类别2",
        "sub_hazard_class_t": "副危险类别3",
        "sysId": "系统配置编号",
        "sysName": "系统配置名称",
        "sysValue": "系统配置值",
        "tLV": "阈限值(PPM)",
        "tableName": "表名",
        "takeorally": "口服",
        "tankCapacity": "舱室容量(m3)",
        "tankFirst": "横向位置",
        "tankID": "舱室序号",
        "tankId": "舱室序号",
        "tankInerting": "液舱是否惰化",
        "tankInfo": "舱柜信息",
        "tankNo": "罐柜编号(无用)",
        "tankSecond": "纵向位置",
        "tankShipNo": "罐柜船检证书编号",
        "tankStructure": "舱室结构",
        "tankThird": "垂直位置",
        "tankWashing": "清洗液货舱作业水洗(是/否)",
        "tankWaterCode": "压载/污水舱室编号",
        "tank_info": "舱柜信息",
        "task_type": "任务类型",
        "tasktype": "过境类型",
        "tel": "联系电话",
        "telNo": "联系电话",
        "tel_no": "联系电话",
        "telePhone": "手机号码",
        "tele_phone": "手机号码",
        "tempInspectDate": "期间检验日期(CCYYMMDD)",
        "tempeRange": "航行时间超过添加剂有效期时，应采取的措施",
        "tempe_range": "温度范围",
        "temperature": "自燃温度",
        "tonnage": "载重吨（吨）",
        "totWeight": "货物总重量（吨）",
        "tot_weight": "总重量",
        "totalTon": "总吨（吨）",
        "total_ton": "总吨位",
        "tradeFlag": "内外贸标志",
        "trade_flag": "贸易标志",
        "trainDate": "培训日期",
        "trainOrg": "培训单位",
        "train_date": "培训时间（yyyy-MM-dd）",
        "train_org": "培训单位",
        "transCargoowner": "货主",
        "transCargoownerCode": "货主备案代码",
        "transHavingCert": "是否含有货物对应的证书",
        "transLoadPort": "装货港口名称",
        "transLoadPortId": "装货港口代码",
        "transNo": "运输单证编号",
        "transOperPlaceCode": "作业码头代码",
        "transShippingNameCN": "正确运输名称(中文)",
        "transShippingNameEN": "正确运输名称(英文)",
        "transTankFirst": "横向位置",
        "transTankId": "舱室序号",
        "transTankSecond": "纵向位置",
        "transTankThird": "垂直位置",
        "transTotWeight": "货物重量",
        "transTradeFlag": "内外贸标志",
        "transUnLoadPort": "卸货港口名称",
        "transUnLoadPortId": "卸货港口代码",
        "transitId": "过境序号",
        "transitType": "过境类型",
        "trashFlag": "含废弃物",
        "treatCompanyCode": "拟送处置单位",
        "trimming": "平舱程序",
        "trimmingProc": "平舱程序",
        "uNNo": "联合国危险品编号",
        "uNNo1": "国内危险品编号",
        "unLoadPort": "卸货港口名称",
        "unLoadPortId": "卸货港口代码",
        "unNo": "联合国危险品编号",
        "unNo1": "国内危险品编号",
        "un_load_port": "卸货港",
        "un_no": "联合国危险品编号",
        "unitId": "成组件序号",
        "unitNo": "车辆牌号",
        "unitSize": "集装箱/罐柜尺寸",
        "unitSizeDetail": "集装箱/罐柜尺寸标准码",
        "unitTypeId": "组件类型编号",
        "unitno": "组件标识号",
        "unloadPort": "卸货港名称",
        "unloadPortCode": "卸货港代码",
        "unloadPortId": "卸货港代码",
        "unloadPortName": "卸货港名称",
        "upLoadFlag": "装/卸载船标记",
        "updFlag": "更新标志",
        "upd_flag": "更新标志",
        "updateTime": "更新时间",
        "update_time": "更新时间",
        "uploadFlag": "装/卸载船标志",
        "urgentAddr": "紧急联系人地址",
        "urgentEmail": "紧急联系人邮箱",
        "urgentFax": "紧急联系人传真",
        "urgentLtd": "紧急联系人公司名称",
        "urgentName": "紧急联系人名称",
        "urgentTel": "紧急联系人电话",
        "userId": "用户id",
        "userName": "用户名称",
        "userNo": "用户编号",
        "user_id": "用户id",
        "user_name": "用户名称",
        "user_no": "用户编号",
        "uummLoginId": "UUMM系统中登录名",
        "uumm_login_id": "UUMM系统中登录名",
        "vESSEL": "船名",
        "vESS_CALL": "船舶呼号",
        "vESS_CODE": "船舶编号",
        "vESS_DIRECTION": "航向",
        "vESS_ID": "船舶初始登记号",
        "vESS_TYPE": "船舶类型",
        "vOYAGE": "航次",
        "valid": "是否有效",
        "validDate": "附件有效期",
        "vapourDensity": "蒸汽密度",
        "vapourPress": "蒸汽压力",
        "vapourPressure": "蒸汽压力",
        "vehicleCertNo": "车载危险品货物证明书编号",
        "vehicleNo": "车辆编号(无用)",
        "vessCode": "船舶代码",
        "vessDirection": "船舶进出港标志",
        "vessId": "船舶初始登记号",
        "vessType": "船舶类型",
        "vess_code": "船舶代码",
        "vess_direction": "船舶进出港标志",
        "vess_id": "船舶初始登记号",
        "vess_type": "船舶类型",
        "vessel": "船名",
        "vesselCall": "装卸载船呼号",
        "vesselFitCertValid": "船舶适载证书是否有效",
        "vesselReq": "载运船要求",
        "vesselType": "船舶类型",
        "vessel_call": "船舶呼号",
        "vessel_req": "载运船要求",
        "vessel_type": "船舶类型",
        "viceHazardClass": "副危险类别",
        "visCosity": "在作业温度下的粘度",
        "visCosityUnit": "粘度单位",
        "voyage": "装卸载船航次",
        "voyageCancelFlag": "船期撤消状态",
        "voyageId": "船期序号",
        "voyageSendTime": "船期发送时间",
        "voyageStatus": "船期发布状态",
        "washingFlag": "是否进行洗舱",
        "wasteLiquid": "预计洗舱废液数量",
        "waterCategory": "水质种类",
        "waterLimit": "适运水份极限百分比",
        "waterPercent": "运输时水份含量百分比",
        "yearInspectDate": "年度检验日期(CCYYMMDD)",
        "zip": "邮编",
        "zipNo": "邮编",
        "zip_no": "邮编",
        "序号": "Desc",
    }

    # 转换为驼峰命名
    camel_case = field_name[0].lower() + field_name[1:] if field_name else field_name
    
    # 查找映射
    if camel_case in mapping:
        return mapping[camel_case]
    
    # 如果没有找到映射，智能理解并翻译字段名
    return smart_translate_field_name(field_name)

def smart_translate_field_name(field_name):
    """智能理解并翻译字段名为中文"""
    # 常见英文单词映射
    word_mapping = {
        "id": "ID",
        "name": "名称",
        "code": "代码",
        "type": "类型",
        "status": "状态",
        "desc": "描述",
        "description": "描述",
        "remark": "备注",
        "address": "地址",
        "tel": "电话",
        "phone": "电话",
        "email": "邮箱",
        "fax": "传真",
        "zip": "邮编",
        "country": "国家",
        "province": "省份",
        "city": "城市",
        "district": "区县",
        "street": "街道",
        "number": "编号",
        "no": "编号",
        "seq": "序号",
        "order": "订单",
        "ship": "船舶",
        "vessel": "船舶",
        "cargo": "货物",
        "port": "港口",
        "dock": "码头",
        "berth": "泊位",
        "tank": "舱柜",
        "bill": "提单",
        "info": "信息",
        "owner": "所有者",
        "company": "公司",
        "user": "用户",
        "create": "创建",
        "update": "更新",
        "delete": "删除",
        "cancel": "取消",
        "finish": "完成",
        "complete": "完成",
        "start": "开始",
        "end": "结束",
        "begin": "开始",
        "time": "时间",
        "date": "日期",
        "year": "年",
        "month": "月",
        "day": "日",
        "hour": "时",
        "minute": "分",
        "second": "秒",
        "amount": "金额",
        "price": "价格",
        "quantity": "数量",
        "weight": "重量",
        "ton": "吨",
        "length": "长度",
        "width": "宽度",
        "height": "高度",
        "depth": "深度",
        "area": "面积",
        "volume": "体积",
        "capacity": "容量",
        "speed": "速度",
        "distance": "距离",
        "direction": "方向",
        "position": "位置",
        "location": "位置",
        "coordinate": "坐标",
        "latitude": "纬度",
        "longitude": "经度",
        "altitude": "海拔",
        "temperature": "温度",
        "pressure": "压力",
        "humidity": "湿度",
        "wind": "风",
        "rain": "雨",
        "snow": "雪",
        "fog": "雾",
        "cloud": "云",
        "sun": "太阳",
        "moon": "月亮",
        "star": "星星",
        "earth": "地球",
        "sea": "海",
        "ocean": "海洋",
        "river": "河流",
        "lake": "湖泊",
        "mountain": "山脉",
        "hill": "丘陵",
        "plain": "平原",
        "plateau": "高原",
        "basin": "盆地",
        "valley": "山谷",
        "canyon": "峡谷",
        "desert": "沙漠",
        "forest": "森林",
        "grass": "草地",
        "field": "田野",
        "farm": "农场",
        "garden": "花园",
        "park": "公园",
        "zoo": "动物园",
        "museum": "博物馆",
        "library": "图书馆",
        "school": "学校",
        "hospital": "医院",
        "bank": "银行",
        "shop": "商店",
        "market": "市场",
        "restaurant": "餐厅",
        "hotel": "酒店",
        "airport": "机场",
        "station": "车站",
        "port": "港口",
        "harbor": "港湾",
        "bridge": "桥梁",
        "tunnel": "隧道",
        "road": "道路",
        "street": "街道",
        "highway": "高速公路",
        "railway": "铁路",
        "subway": "地铁",
        "bus": "公交",
        "taxi": "出租车",
        "car": "汽车",
        "truck": "卡车",
        "train": "火车",
        "plane": "飞机",
        "ship": "船舶",
        "boat": "小船",
        "bicycle": "自行车",
        "motorcycle": "摩托车",
        "walk": "步行",
        "run": "跑步",
        "swim": "游泳",
        "fly": "飞行",
        "drive": "驾驶",
        "ride": "骑行",
        "sail": "航行",
        "row": "划船",
        "fish": "钓鱼",
        "hunt": "打猎",
        "camp": "露营",
        "hike": "徒步",
        "climb": "登山",
        "ski": "滑雪",
        "skate": "滑冰",
        "surf": "冲浪",
        "dive": "潜水",
        "jump": "跳跃",
        "dance": "跳舞",
        "sing": "唱歌",
        "play": "演奏",
        "listen": "听",
        "watch": "观看",
        "read": "阅读",
        "write": "写作",
        "draw": "绘画",
        "paint": "绘画",
        "photo": "摄影",
        "video": "视频",
        "audio": "音频",
        "image": "图像",
        "file": "文件",
        "document": "文档",
        "data": "数据",
        "database": "数据库",
        "table": "表",
        "column": "列",
        "row": "行",
        "cell": "单元格",
        "sheet": "工作表",
        "workbook": "工作簿",
        "excel": "Excel",
        "word": "Word",
        "powerpoint": "PowerPoint",
        "pdf": "PDF",
        "html": "HTML",
        "xml": "XML",
        "json": "JSON",
        "csv": "CSV",
        "txt": "TXT",
        "log": "日志",
        "config": "配置",
        "setting": "设置",
        "option": "选项",
        "parameter": "参数",
        "argument": "参数",
        "variable": "变量",
        "constant": "常量",
        "function": "函数",
        "method": "方法",
        "class": "类",
        "object": "对象",
        "instance": "实例",
        "property": "属性",
        "attribute": "属性",
        "element": "元素",
        "node": "节点",
        "edge": "边",
        "graph": "图",
        "tree": "树",
        "list": "列表",
        "array": "数组",
        "set": "集合",
        "map": "映射",
        "dictionary": "字典",
        "hash": "哈希",
        "queue": "队列",
        "stack": "栈",
        "heap": "堆",
        "tree": "树",
        "graph": "图",
        "network": "网络",
        "server": "服务器",
        "client": "客户端",
        "browser": "浏览器",
        "app": "应用",
        "application": "应用程序",
        "system": "系统",
        "platform": "平台",
        "framework": "框架",
        "library": "库",
        "package": "包",
        "module": "模块",
        "component": "组件",
        "control": "控件",
        "widget": "小部件",
        "layout": "布局",
        "style": "样式",
        "theme": "主题",
        "color": "颜色",
        "font": "字体",
        "size": "大小",
        "scale": "比例",
        "ratio": "比率",
        "percent": "百分比",
        "fraction": "分数",
        "decimal": "小数",
        "integer": "整数",
        "float": "浮点数",
        "double": "双精度",
        "long": "长整型",
        "short": "短整型",
        "byte": "字节",
        "char": "字符",
        "string": "字符串",
        "boolean": "布尔值",
        "true": "真",
        "false": "假",
        "null": "空",
        "void": "无",
        "empty": "空",
        "blank": "空白",
        "space": "空格",
        "tab": "制表符",
        "newline": "换行符",
        "return": "回车符",
        "escape": "转义符",
        "quote": "引号",
        "apostrophe": "撇号",
        "comma": "逗号",
        "period": "句号",
        "semicolon": "分号",
        "colon": "冒号",
        "exclamation": "感叹号",
        "question": "问号",
        "asterisk": "星号",
        "slash": "斜杠",
        "backslash": "反斜杠",
        "pipe": "竖线",
        "underscore": "下划线",
        "hyphen": "连字符",
        "plus": "加号",
        "minus": "减号",
        "multiply": "乘号",
        "divide": "除号",
        "equal": "等号",
        "greater": "大于",
        "less": "小于",
        "and": "与",
        "or": "或",
        "not": "非",
        "if": "如果",
        "else": "否则",
        "for": "对于",
        "while": "当",
        "do": "做",
        "case": "情况",
        "switch": "开关",
        "break": "中断",
        "continue": "继续",
        "return": "返回",
        "throw": "抛出",
        "catch": "捕获",
        "try": "尝试",
        "finally": "最终",
        "import": "导入",
        "export": "导出",
        "public": "公共",
        "private": "私有",
        "protected": "受保护",
        "static": "静态",
        "final": "最终",
        "abstract": "抽象",
        "interface": "接口",
        "extends": "继承",
        "implements": "实现",
        "override": "重写",
        "overload": "重载",
        "new": "新",
        "old": "旧",
        "current": "当前",
        "previous": "上一个",
        "next": "下一个",
        "first": "第一个",
        "last": "最后一个",
        "min": "最小",
        "max": "最大",
        "avg": "平均",
        "sum": "总和",
        "count": "计数",
        "total": "总计",
        "sub": "子",
        "super": "父",
        "this": "这个",
        "that": "那个",
        "these": "这些",
        "those": "那些",
        "some": "一些",
        "any": "任何",
        "all": "所有",
        "none": "无",
        "both": "两者",
        "either": "任一",
        "neither": "两者都不",
        "each": "每个",
        "every": "每个",
        "other": "其他",
        "another": "另一个",
        "same": "相同",
        "different": "不同",
        "similar": "相似",
        "equal": "相等",
        "greater": "大于",
        "less": "小于",
        "before": "之前",
        "after": "之后",
        "during": "期间",
        "within": "在...内",
        "without": "没有",
        "with": "有",
        "from": "来自",
        "to": "到",
        "by": "通过",
        "through": "通过",
        "via": "通过",
        "using": "使用",
        "used": "已使用",
        "unused": "未使用",
        "enabled": "已启用",
        "disabled": "已禁用",
        "active": "活动",
        "inactive": "非活动",
        "visible": "可见",
        "invisible": "不可见",
        "show": "显示",
        "hide": "隐藏",
        "open": "打开",
        "close": "关闭",
        "save": "保存",
        "load": "加载",
        "read": "读取",
        "write": "写入",
        "delete": "删除",
        "create": "创建",
        "update": "更新",
        "insert": "插入",
        "remove": "移除",
        "add": "添加",
        "append": "追加",
        "prepend": "前置",
        "merge": "合并",
        "split": "分割",
        "join": "连接",
        "concat": "连接",
        "replace": "替换",
        "substitute": "替换",
        "copy": "复制",
        "paste": "粘贴",
        "cut": "剪切",
        "undo": "撤销",
        "redo": "重做",
        "clear": "清除",
        "reset": "重置",
        "refresh": "刷新",
        "reload": "重新加载",
        "restart": "重新启动",
        "shutdown": "关闭",
        "startup": "启动",
        "boot": "引导",
        "login": "登录",
        "logout": "登出",
        "register": "注册",
        "signup": "注册",
        "signin": "登录",
        "signout": "登出",
        "auth": "认证",
        "permission": "权限",
        "role": "角色",
        "group": "组",
        "team": "团队",
        "department": "部门",
        "division": "部门",
        "section": "部门",
        "unit": "单位",
        "item": "项目",
        "product": "产品",
        "service": "服务",
        "resource": "资源",
        "asset": "资产",
        "liability": "负债",
        "equity": "权益",
        "revenue": "收入",
        "expense": "支出",
        "profit": "利润",
        "loss": "损失",
        "budget": "预算",
        "forecast": "预测",
        "plan": "计划",
        "schedule": "日程",
        "calendar": "日历",
        "agenda": "议程",
        "task": "任务",
        "job": "工作",
        "work": "工作",
        "project": "项目",
        "milestone": "里程碑",
        "goal": "目标",
        "objective": "目标",
        "strategy": "策略",
        "tactic": "战术",
        "policy": "政策",
        "rule": "规则",
        "regulation": "法规",
        "law": "法律",
        "contract": "合同",
        "agreement": "协议",
        "treaty": "条约",
        "license": "许可证",
        "certificate": "证书",
        "diploma": "文凭",
        "degree": "学位",
        "education": "教育",
        "experience": "经验",
        "skill": "技能",
        "ability": "能力",
        "talent": "天赋",
        "knowledge": "知识",
        "wisdom": "智慧",
        "intelligence": "智力",
        "memory": "记忆",
        "thought": "思想",
        "idea": "想法",
        "concept": "概念",
        "theory": "理论",
        "practice": "实践",
        "experiment": "实验",
        "test": "测试",
        "debug": "调试",
        "error": "错误",
        "warning": "警告",
        "info": "信息",
        "success": "成功",
        "failure": "失败",
        "exception": "异常",
        "bug": "缺陷",
        "issue": "问题",
        "problem": "问题",
        "solution": "解决方案",
        "answer": "答案",
        "question": "问题",
        "help": "帮助",
        "support": "支持",
        "assistance": "协助",
        "guidance": "指导",
        "instruction": "指示",
        "direction": "方向",
        "manual": "手册",
        "guide": "指南",
        "tutorial": "教程",
        "example": "示例",
        "sample": "样本",
        "template": "模板",
        "pattern": "模式",
        "format": "格式",
        "structure": "结构",
        "architecture": "架构",
        "design": "设计",
        "model": "模型",
        "schema": "模式",
        "protocol": "协议",
        "standard": "标准",
        "specification": "规范",
        "requirement": "要求",
        "constraint": "约束",
        "limit": "限制",
        "boundary": "边界",
        "edge": "边缘",
        "corner": "角落",
        "center": "中心",
        "middle": "中间",
        "top": "顶部",
        "bottom": "底部",
        "left": "左侧",
        "right": "右侧",
        "front": "前面",
        "back": "后面",
        "inside": "内部",
        "outside": "外部",
        "above": "上方",
        "below": "下方",
        "between": "之间",
        "among": "之中",
        "around": "周围",
        "near": "附近",
        "far": "远处",
        "close": "关闭",
        "open": "打开",
        "locked": "已锁定",
        "unlocked": "已解锁",
        "secure": "安全",
        "insecure": "不安全",
        "safe": "安全",
        "dangerous": "危险",
        "risky": "有风险",
        "stable": "稳定",
        "unstable": "不稳定",
        "reliable": "可靠",
        "unreliable": "不可靠",
        "available": "可用",
        "unavailable": "不可用",
        "ready": "就绪",
        "notready": "未就绪",
        "pending": "待处理",
        "processing": "处理中",
        "completed": "已完成",
        "incomplete": "未完成",
        "partial": "部分",
        "full": "完整",
        "total": "总计",
        "subtotal": "小计",
        "grand": "总计",
        "net": "净值",
        "gross": "毛值",
        "tax": "税",
        "fee": "费用",
        "charge": "收费",
        "cost": "成本",
        "price": "价格",
        "rate": "费率",
        "discount": "折扣",
        "bonus": "奖金",
        "penalty": "惩罚",
        "fine": "罚款",
        "interest": "利息",
        "principal": "本金",
        "balance": "余额",
        "amount": "金额",
        "quantity": "数量",
        "quality": "质量",
        "grade": "等级",
        "level": "级别",
        "rank": "排名",
        "score": "分数",
        "point": "分数",
        "mark": "标记",
        "flag": "标志",
        "tag": "标签",
        "label": "标签",
        "category": "类别",
        "class": "类别",
        "type": "类型",
        "kind": "种类",
        "sort": "种类",
        "group": "组",
        "set": "集合",
        "list": "列表",
        "array": "数组",
        "collection": "集合",
        "map": "映射",
        "dictionary": "字典",
        "hash": "哈希",
        "table": "表",
        "view": "视图",
        "query": "查询",
        "filter": "过滤器",
        "sorter": "排序器",
        "comparator": "比较器",
        "iterator": "迭代器",
        "enumerator": "枚举器",
        "generator": "生成器",
        "factory": "工厂",
        "builder": "构建器",
        "prototype": "原型",
        "singleton": "单例",
        "instance": "实例",
        "object": "对象",
        "class": "类",
        "interface": "接口",
        "abstract": "抽象",
        "final": "最终",
        "static": "静态",
        "public": "公共",
        "private": "私有",
        "protected": "受保护",
        "package": "包",
        "import": "导入",
        "export": "导出"
    }
    
    # 将字段名拆分为单词并翻译
    words = []
    current_word = ""
    
    for char in field_name:
        if char.isupper():
            if current_word:
                words.append(current_word)
            current_word = char.lower()
        else:
            current_word += char.lower()
    
    if current_word:
        words.append(current_word)
    
    # 翻译每个单词
    translated_words = []
    for word in words:
        if word in word_mapping:
            translated_words.append(word_mapping[word])
        else:
            # 如果没有找到映射，保留原单词
            translated_words.append(word)
    
    # 组合翻译结果
    if not translated_words:
        return field_name
    
    # 如果只有一个单词，直接返回
    if len(translated_words) == 1:
        return translated_words[0]
    
    # 如果有多个单词，组合它们
    return ''.join(translated_words)

def add_borders_to_worksheet(worksheet):
    """为工作表中所有有数据的单元格添加边框"""
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.border = thin_border

def generate_excel_for_folder(folder_path, output_filename):
    """为指定文件夹生成Excel数据字典"""
    po_files = list(Path(folder_path).glob("*PO.java"))
    
    if not po_files:
        print(f"文件夹 {folder_path} 中没有找到PO文件")
        return
    
    print(f"正在处理文件夹: {folder_path}")
    print(f"找到 {len(po_files)} 个PO文件")
    
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        for po_file in po_files:
            table_name, fields = parse_po_file(po_file)
            
            if not fields:
                print(f"警告: {po_file.name} 没有找到字段信息")
                continue
            
            # 创建DataFrame - 字段名放在第一列，中文名称放在第二列
            data = []
            for field in fields:
                data.append([
                    field["column"],
                    field["chinese_name"],  # 第二列：中文名称
                    field["data_type"],
                    field["pk_index"],
                    field["remark"],
                    field["is_required"]
                ])
            
            df = pd.DataFrame(data, columns=["字段名", "中文名称", "列名", "数据类型", "PK/INDEX", "备注", "是否必填"])
            
            # 限制sheet名长度（Excel限制为31个字符）
            safe_sheet_name = table_name[:31]
            
            # 写入Excel
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
            
            # 获取工作表并添加边框
            worksheet = writer.sheets[safe_sheet_name]
            add_borders_to_worksheet(worksheet)
            
            # 调整列宽
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            print(f"  - 已处理: {po_file.name} -> {safe_sheet_name} ({len(fields)} 个字段)")
    
    print(f"\nExcel文件已生成: {output_filename}")
    print(f"包含 {len(po_files)} 个工作表")

def main():
    """主函数 - 支持命令行参数或自动扫描"""
    import sys
    
    base_path = Path(__file__).parent
    
    # 方式1: 使用命令行参数指定文件夹
    if len(sys.argv) > 1:
        for folder_name in sys.argv[1:]:
            folder_path = base_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                output_file = base_path / f"{folder_name}数据字典.xlsx"
                generate_excel_for_folder(folder_path, output_file)
            else:
                print(f"文件夹不存在: {folder_name}")
    else:
        # 方式2: 自动扫描当前目录下所有包含PO文件的文件夹
        print("未指定文件夹，自动扫描当前目录下包含PO文件的文件夹...\n")
        
        # 查找所有包含PO文件的子文件夹
        folders_with_po = []
        for item in base_path.iterdir():
            if item.is_dir():
                po_files = list(item.glob("*PO.java"))
                if po_files:
                    folders_with_po.append(item)
        
        if not folders_with_po:
            print("未找到包含PO文件的文件夹")
            return
        
        # 处理每个文件夹
        for folder in folders_with_po:
            output_file = base_path / f"{folder.name}数据字典.xlsx"
            generate_excel_for_folder(folder, output_file)
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
```

## 使用方法

### 1. 环境要求

- Python 3.6+
- 依赖库：
  - pandas
  - openpyxl

### 2. 安装依赖

```bash
pip install pandas openpyxl
```

### 3. 创建脚本文件

将上面的完整代码保存为 `generate_po_dictionaries.py` 文件。

### 4. 运行脚本

#### 方式1: 指定文件夹处理（推荐）

```bash
# 处理单个文件夹
python generate_po_dictionaries.py my_folder

# 处理多个文件夹
python generate_po_dictionaries.py folder1 folder2 folder3
```

#### 方式2: 自动扫描所有包含PO文件的文件夹

```bash
# 不指定参数，自动扫描当前目录下所有包含PO文件的文件夹
python generate_po_dictionaries.py
```

### 5. 输出结果

脚本会根据处理方式生成不同的输出：

**指定文件夹时：**
- 为每个指定的文件夹生成一个Excel文件
- 文件名格式：`{文件夹名}数据字典.xlsx`
- 例如：`python generate_po_dictionaries.py my_folder` 会生成 `my_folder数据字典.xlsx`

**自动扫描时：**
- 为每个包含PO文件的文件夹生成一个Excel文件
- 文件名格式：`{文件夹名}数据字典.xlsx`
- 例如：如果扫描到 `decl` 和 `ship` 文件夹，会生成 `decl数据字典.xlsx` 和 `ship数据字典.xlsx`

## 数据类型转换规则

| Java类型 | Oracle数据类型 | 说明 |
|---------|--------------|------|
| String | VARCHAR2(length char) | 使用@Column注解中的length属性 |
| Long | NUMBER(length) | 使用@Column注解中的length属性，默认16 |
| Integer | NUMBER(length) | 使用@Column注解中的length属性，默认10 |
| Float | NUMBER(length) | 使用@Column注解中的length属性，默认10,2 |
| Double | NUMBER(length) | 使用@Column注解中的length属性，默认10,2 |
| Date | DATE | 日期类型 |

## 输出格式

生成的Excel文件包含以下列：

| 列名 | 说明 |
|------|------|
| 字段名 | Java字段名（原始字段名） |
| 中文名称 | 智能翻译后的中文名称 |
| 列名 | 数据库字段名（来自@Column注解的name属性） |
| 数据类型 | 转换后的Oracle数据类型 |
| PK/INDEX | 主键标识（"pk"表示主键） |
| 备注 | 序列生成器信息或其他备注 |
| 是否必填 | 根据nullable属性判断（"必填"或空） |

## 自定义配置

### 处理其他文件夹

现在脚本支持两种使用方式：

#### 方式1: 命令行参数（推荐）

```bash
# 处理单个文件夹
python generate_po_dictionaries.py folder_name

# 处理多个文件夹
python generate_po_dictionaries.py folder1 folder2 folder3
```

#### 方式2: 自动扫描

不提供参数时，脚本会自动扫描当前目录下所有包含PO文件的子文件夹。

### 修改输出路径

如果需要修改输出文件的位置或名称，可以修改`main()`函数中的输出逻辑：

```python
# 修改输出路径
output_file = Path("/your/custom/path") / f"{folder.name}数据字典.xlsx"
```

### 添加更多字段映射

如果需要添加更多字段的中文名称映射，可以修改`generate_chinese_name()`函数中的`mapping`字典：

```python
mapping = {
    "id": "主键ID",
    "yourFieldName": "你的字段中文名",
    # 添加更多映射...
}
```

### 修改数据类型转换

如果需要修改数据类型转换规则，可以修改`convert_data_type()`函数：

```python
def convert_data_type(java_type, length):
    """转换Java数据类型为Oracle数据类型"""
    if java_type == "YourType":
        if length:
            return f"YOUR_TYPE({length})"
        return "YOUR_TYPE(default)"
    # 添加更多类型转换...
```

## 示例输出

### Excel工作表结构

| 字段名 | 中文名称 | 列名 | 数据类型 | PK/INDEX | 备注 | 是否必填 |
|---------|---------|------|---------|----------|------|---------|
| id | 主键ID | ID | NUMBER(16) | pk | 对应SEQ_HSXMDECL_ADDITIVE_INFO | 必填 |
| aplId | 申请ID | APL_ID | VARCHAR2(25 char) | | | |
| produceDate | 生产日期 | PRODUCE_DATE | VARCHAR2(10 char) | | | |
| company | 公司 | COMPANY | VARCHAR2(70 char) | | | |

## 注意事项

1. PO文件必须使用JPA注解（@Entity, @Table, @Column等）
2. @Table注解中的name属性用于确定表名
3. @Column注解中的name属性用于确定列名
4. @Id注解用于标识主键字段
5. nullable属性用于判断字段是否必填
6. length属性用于确定字符串和数字类型的长度

## 常见问题

### Q: 为什么有些字段没有中文名称？

A: 脚本会根据字段名智能翻译成中文。如果字段名不在预定义的映射表中，会使用智能单词翻译功能。可以在`generate_chinese_name()`函数中添加更多的字段映射。

### Q: 如何修改数据类型转换规则？

A: 可以修改`convert_data_type()`函数来调整数据类型转换逻辑。

### Q: 如何处理多个文件夹？

A: 可以在`main()`函数中添加更多的文件夹处理逻辑，或者直接调用`generate_excel_for_folder()`函数处理指定文件夹。

### Q: 支持哪些Java类型？

A: 目前支持String, Long, Integer, Float, Double, Date等常见类型。如需支持其他类型，可以在`convert_data_type()`函数中添加转换规则。

### Q: Excel文件中的Sheet名称太长怎么办？

A: 脚本会自动截断表名到31个字符（Excel的限制）。如果需要更长的名称，可以修改`safe_sheet_name = table_name[:31]`这一行。

## 技术实现

- 使用正则表达式解析Java注解
- 使用pandas进行数据处理
- 使用openpyxl进行Excel文件生成和格式化
- **智能字段名翻译**：自动将字段名拆分为单词并翻译
- **优化的列顺序**：字段名放在第一列，中文名称放在第二列
- 自动识别主键和必填字段
- 自动添加边框和调整列宽

## 快速开始

### 方式1: 指定文件夹处理（推荐）

1. 复制上面的完整代码
2. 保存为 `generate_po_dictionaries.py`
3. 安装依赖：`pip install pandas openpyxl`
4. 将PO文件放在任意文件夹中（例如：`my_po_folder`）
5. 运行脚本指定文件夹：
   ```bash
   python generate_po_dictionaries.py my_po_folder
   ```
6. 查看生成的 `my_po_folder数据字典.xlsx` 文件

### 方式2: 自动扫描所有文件夹

1. 复制上面的完整代码
2. 保存为 `generate_po_dictionaries.py`
3. 安装依赖：`pip install pandas openpyxl`
4. 将PO文件放在多个文件夹中（例如：`folder1`, `folder2`, `folder3`）
5. 运行脚本不指定参数：
   ```bash
   python generate_po_dictionaries.py
   ```
6. 查看生成的多个Excel文件（每个文件夹一个）

### 处理多个文件夹

```bash
# 一次性处理多个文件夹
python generate_po_dictionaries.py folder1 folder2 folder3
```
#include "stdafx.h"
#include "GTJDomainModel/Const/GFYType.h"
#include "GTJDomainModel/Common/GFYCommon.h"
#include "GMPCore/GMPMainForm.h"
#include "GMPProject/GMPModelDictManager.h"
#include "IGMPPropertySchema.h"
#include "GMath/GMatrix4.h"
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

using namespace ggp;

int getSubType(IGMPElementDrawObj *pEdo)
{
    const wchar_t *elementSubTypeName = pfnType;
    switch (pEdo->elementType())
    {
    case etBeam:
    case etStripFD: {
        elementSubTypeName = pfnType1;
        break;
    }
    case etWall: {
        elementSubTypeName = pfnInnerOuterFlag;
        break;
    }
    }

    GMPPropPtr pProptrFirst = pEdo->properties()->propByName(elementSubTypeName);
    return pProptrFirst ? pProptrFirst->asInteger() : 0;
}

struct PropertyInfo
{
    QString code;
    QString description;
    int     dataType;
    QString value;
    int     orderNum;
    bool    publicFlag;
};

QJsonObject propertyInfoToJson(const PropertyInfo &prop)
{
    QJsonObject obj;
    obj["code"] = prop.code;
    obj["description"] = prop.description;
    obj["dataType"]    = prop.dataType;
    obj["value"]       = prop.value;
    obj["orderNum"]    = prop.orderNum;
    obj["publicFlag"]  = prop.publicFlag;
    return obj;
}

PropertyInfo getProperty(GMPPropPtr pProperty)
{
    PropertyInfo info;
    info.code        = pProperty->schema()->code();
    info.description = pProperty->schema()->description();
    info.dataType    = pProperty->schema()->dataType();
    info.orderNum    = pProperty->schema()->orderNum();
    info.publicFlag =  pProperty->schema()->publicFlag();

    switch (pProperty->schema()->dataType())
    {
    case gmdtBoolean: {
        info.value = QString::number(pProperty->asBoolean());
        break;
    }
    case gmdtLongInt:
    case gmdtShortInt:
    case gmdtByte:
    case gmdtSmallInt:
    case gmdtWord:
    case gmdtInt64: {
        info.value = QString::number(pProperty->asInteger());
        break;
    }
    case gmdtDouble:
    case gmdtDecimal: {
        info.value = QString::number(pProperty->asDouble());
        break;
    }
    case gmdtString:
    case gmdtText: {
        info.value = pProperty->asString();
        break;
    }
    default:
        break;
    }

    return info;
}

std::vector<PropertyInfo> getProperties(IGMPElementDrawObj *pEdo)
{
    std::vector<PropertyInfo> vProperties;
    if (!pEdo)
        return vProperties;

    auto pProperties = pEdo->properties();
    if (!pProperties)
        return vProperties;

    for (int i = 0, nLen = pProperties->count(); i < nLen; ++i)
    {
        auto pProp = pProperties->prop(i);
        auto propInfo = getProperty(pProp);
        vProperties.emplace_back(std::move(propInfo));
    }

    return vProperties;
}

QJsonArray getPropertiesJson(IGMPElementDrawObj *pEdo)
{
    QJsonArray jsonArray;
    if (!pEdo)
    {
        return jsonArray;
    }

    auto vProperties = getProperties(pEdo);
    for (auto &item : vProperties)
    {
        jsonArray.append(propertyInfoToJson(item));
    }

    return jsonArray;
}

void getShape(IGMPElementDrawObj *pEdo, QString& szShape, QString& szBody)
{
    IGMPShape *pShape = pEdo->shape();
    if (!pShape)
        return;

    auto coord = pShape->coordinate();
    CMatrix4d oMatrix;
    coord.GetWorldMatrix(oMatrix);

    ggp::CPolygonPtr pPoly;
    ggp::CBodyPtr    pBody;

    if (pShape->shapeClass() == scFace)
    {
        IGMPFaceSolidShape *pSolidShape = dynamic_cast<IGMPFaceSolidShape *>(pShape);
        if (pSolidShape && pSolidShape->poly())
        {
            pPoly = pSolidShape->poly()->Clone();
            pBody = pSolidShape->body()->Clone();
        }
    }
    else if (pShape->shapeClass() == scLine)
    {
        auto pLineSolidShape = dynamic_cast<IGMPSectionLineSolidShape *>(pShape);
        if (pLineSolidShape)
        {
            pPoly = pLineSolidShape->poly()->Clone();
        }
    }

    if (pPoly.valid())
    {
        pPoly->Transform(oMatrix);
        szShape = pPoly->AsString();
    }

    if (pBody.valid())
    {
        szBody = pBody->AsString();
    }
}

QJsonObject getEdoJson(int64_t edoId)
{
    QJsonObject obj;

    IGMPElementDrawObj *pEdo = nullptr;
    IGMPServiceMgr *pServiceMgr = g_pGMPMainForm->serviceMgr();
    IGMPService    *pService    = g_pGMPMainForm->service();
    if (pServiceMgr && pService)
    {
        pEdo = pService->model()->edoContnr()->find(edoId);
    }

    if (!pEdo)
    {
        return obj;
    }

    obj["description"] = pEdo->properties()->propByName(pfnDescription)->asString();
    obj["elementType"] = pEdo->elementType();
    obj["elementSubType"] = pEdo->elementSubType();

    QString szSubTypeName;
    auto typeInfo = GMPModelDictManager::getInstance()->elementTypeInfo(pEdo->elementType());
    for (auto subTypeInfo : typeInfo.listSubTypeInfos)
    {
        if (subTypeInfo.nElementSubTypeID == pEdo->elementSubType())
        {
            szSubTypeName = subTypeInfo.strSubTypeName;
            break;
        }
    }

    obj["typeName"] = typeInfo.strTypeName;
    obj["subTypeName"] = szSubTypeName;
    obj["properties"] = getPropertiesJson(pEdo);

    QString szShape, szBody;
    getShape(pEdo, szShape, szBody);
    obj["shape"] = szShape;
    obj["body"]  = szBody;

    return obj;
}

std::string getEdo(int64_t edoId)
{
    auto obj = getEdoJson(edoId);

    QJsonDocument jsonDoc(obj);
    auto jsonString = jsonDoc.toJson(QJsonDocument::Indented);
    return jsonString.toStdString();
}

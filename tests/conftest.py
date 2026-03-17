"""Test fixtures: synthetic DDR XML for testing."""

from __future__ import annotations

from pathlib import Path

import pytest

SAMPLE_DDR_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<FMPReport link="FMPReport" type="Report" version="19">
  <File name="TestSolution" path="/path/to/TestSolution.fmp12">
    <BaseTableCatalog>
      <BaseTable id="1065089" name="Contacts" records="150">
        <FieldCatalog>
          <Field id="1" name="PrimaryKey" fieldType="Normal" dataType="Text"/>
          <Field id="2" name="FirstName" fieldType="Normal" dataType="Text"/>
          <Field id="3" name="LastName" fieldType="Normal" dataType="Text"/>
          <Field id="4" name="Email" fieldType="Normal" dataType="Text"/>
          <Field id="5" name="FullName" fieldType="Calculated" dataType="Text"/>
        </FieldCatalog>
      </BaseTable>
      <BaseTable id="1065090" name="Invoices" records="75">
        <FieldCatalog>
          <Field id="1" name="InvoiceID" fieldType="Normal" dataType="Number"/>
          <Field id="2" name="ContactID" fieldType="Normal" dataType="Number"/>
          <Field id="3" name="Amount" fieldType="Normal" dataType="Number"/>
          <Field id="4" name="Date" fieldType="Normal" dataType="Date"/>
        </FieldCatalog>
      </BaseTable>
    </BaseTableCatalog>
    <RelationshipGraph>
      <TableList>
        <Table id="200" name="Contacts" baseTable="Contacts" baseTableId="1065089"/>
        <Table id="201" name="Invoices" baseTable="Invoices" baseTableId="1065090"/>
        <Table id="202" name="Invoices_by_Contact" baseTable="Invoices" baseTableId="1065090"/>
      </TableList>
      <RelationshipList>
        <Relationship id="300">
          <LeftTable id="200" name="Contacts"/>
          <RightTable id="201" name="Invoices"/>
          <JoinPredicateCatalog>
            <JoinPredicate type="equal">
              <LeftField tableOccurrenceId="200" fieldId="1" name="PrimaryKey"/>
              <RightField tableOccurrenceId="201" fieldId="2" name="ContactID"/>
            </JoinPredicate>
          </JoinPredicateCatalog>
        </Relationship>
      </RelationshipList>
    </RelationshipGraph>
    <LayoutCatalog>
      <Layout id="400" name="Contact Detail" includeInMenu="True">
        <TableRef id="200" name="Contacts"/>
        <FieldRef id="2" name="FirstName" repetition="1"/>
        <FieldRef id="3" name="LastName" repetition="1"/>
        <FieldRef id="4" name="Email" repetition="1"/>
      </Layout>
      <Layout id="401" name="Invoice List" includeInMenu="True">
        <TableRef id="201" name="Invoices"/>
        <FieldRef id="1" name="InvoiceID" repetition="1"/>
        <FieldRef id="3" name="Amount" repetition="1"/>
      </Layout>
    </LayoutCatalog>
    <ScriptCatalog>
      <Script id="500" name="Create Invoice" includeInMenu="True">
        <StepList>
          <Step id="89" name="Go to Layout" enable="True">
            <LayoutRef id="401" name="Invoice List"/>
          </Step>
          <Step id="1" name="New Record/Request" enable="True"/>
          <Step id="76" name="Set Field" enable="True">
            <FieldRef id="2" name="ContactID" table="Invoices"/>
          </Step>
        </StepList>
      </Script>
      <Script id="501" name="Navigate to Invoices" includeInMenu="True">
        <StepList>
          <Step id="89" name="Go to Layout" enable="True">
            <LayoutRef id="401" name="Invoice List"/>
          </Step>
          <Step id="6" name="Perform Script" enable="True">
            <ScriptRef id="500" name="Create Invoice"/>
          </Step>
        </StepList>
      </Script>
    </ScriptCatalog>
    <ValueListCatalog>
      <ValueList id="600" name="Contact Names"/>
    </ValueListCatalog>
    <CustomFunctionCatalog>
      <CustomFunction id="700" name="FormatName" parameters="first;last" visible="True"/>
    </CustomFunctionCatalog>
    <CustomMenuCatalog>
      <CustomMenu id="800" name="File Menu"/>
    </CustomMenuCatalog>
    <CustomMenuSetCatalog>
      <CustomMenuSet id="900" name="Default Menu Set"/>
    </CustomMenuSetCatalog>
    <AccountCatalog>
      <Account id="1000" name="Admin" status="Active"/>
    </AccountCatalog>
    <PrivilegeCatalog>
      <PrivilegeSet id="1100" name="Full Access"/>
    </PrivilegeCatalog>
    <ExtendedPrivilegeCatalog>
      <ExtendedPrivilege id="1200" name="fmapp"/>
    </ExtendedPrivilegeCatalog>
    <ExternalDataSourcesCatalog>
      <ExternalDataSource id="1300" name="RemoteDB"/>
    </ExternalDataSourcesCatalog>
  </File>
</FMPReport>
"""


@pytest.fixture
def sample_ddr_xml(tmp_path: Path) -> Path:
    """Write sample DDR XML to a temp file and return its path."""
    xml_path = tmp_path / "TestSolution.xml"
    xml_path.write_text(SAMPLE_DDR_XML, encoding="utf-8")
    return xml_path


@pytest.fixture
def malformed_ddr_xml(tmp_path: Path) -> Path:
    """DDR XML with malformed sections — should not crash."""
    xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<FMPReport>
  <File name="Broken">
    <BaseTableCatalog>
      <BaseTable id="1" name="Good">
        <FieldCatalog>
          <Field id="1" name="OK" fieldType="Normal" dataType="Text"/>
          <Field id="2" name="Broken fieldType="Normal" dataType="Text"/>
          <!-- Malformed: missing closing quote above -->
        </FieldCatalog>
      </BaseTable>
      <BaseTable id="2" name="Also Good">
        <FieldCatalog>
          <Field id="1" name="Fine" fieldType="Normal" dataType="Text"/>
        </FieldCatalog>
      </BaseTable>
    </BaseTableCatalog>
  </File>
</FMPReport>
"""
    xml_path = tmp_path / "Broken.xml"
    xml_path.write_text(xml, encoding="utf-8")
    return xml_path

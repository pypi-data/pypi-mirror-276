'''
# spot-elastigroup-group

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Spot::Elastigroup::Group` v1.0.4.

## Description

The Spot Elastigroup Resource allows you to create, update, manage, and delete Spot Elastigroups easily with CloudFormation

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Spot::Elastigroup::Group \
  --publisher-id 91d05981c6c0b080f2f1adcb370e1145c39b99e2 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/91d05981c6c0b080f2f1adcb370e1145c39b99e2/Spot-Elastigroup-Group \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Spot::Elastigroup::Group`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fspot-elastigroup-group+v1.0.4).
* Issues related to `Spot::Elastigroup::Group` should be reported to the [publisher](undefined).

## License

Distributed under the Apache-2.0 License.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Attribute",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Attribute:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: 
        :param value: 

        :schema: Attribute
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9478cc4b27b054d3ffa8d22ecfb7e1d41ca962813698f0f602875c1fc537d688)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attribute#key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attribute#value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Attribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.AutoScaleDown",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_periods": "evaluationPeriods",
        "max_scale_down_percentage": "maxScaleDownPercentage",
    },
)
class AutoScaleDown:
    def __init__(
        self,
        *,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        max_scale_down_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param evaluation_periods: 
        :param max_scale_down_percentage: 

        :schema: AutoScaleDown
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759f59664e992b5203ff390202cc7fd008d4a185c523c3d8a3884ae137b66d70)
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument max_scale_down_percentage", value=max_scale_down_percentage, expected_type=type_hints["max_scale_down_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if max_scale_down_percentage is not None:
            self._values["max_scale_down_percentage"] = max_scale_down_percentage

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: AutoScaleDown#evaluationPeriods
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_scale_down_percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: AutoScaleDown#maxScaleDownPercentage
        '''
        result = self._values.get("max_scale_down_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScaleDown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.BeanStalkStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "should_drain_instances": "shouldDrainInstances",
    },
)
class BeanStalkStrategy:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        should_drain_instances: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param action: 
        :param should_drain_instances: 

        :schema: BeanStalkStrategy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ac0186c8a145a597deb9b32c8b76bef21257e67d3a1ad963e803e2f3ae9f02)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument should_drain_instances", value=should_drain_instances, expected_type=type_hints["should_drain_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if should_drain_instances is not None:
            self._values["should_drain_instances"] = should_drain_instances

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BeanStalkStrategy#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def should_drain_instances(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: BeanStalkStrategy#shouldDrainInstances
        '''
        result = self._values.get("should_drain_instances")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeanStalkStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.BlockDeviceMapping",
    jsii_struct_bases=[],
    name_mapping={
        "device_name": "deviceName",
        "ebs": "ebs",
        "no_device": "noDevice",
        "virtual_name": "virtualName",
    },
)
class BlockDeviceMapping:
    def __init__(
        self,
        *,
        device_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional[typing.Union["BlockDeviceMappingEbs", typing.Dict[builtins.str, typing.Any]]] = None,
        no_device: typing.Optional[builtins.str] = None,
        virtual_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: 
        :param ebs: 
        :param no_device: 
        :param virtual_name: 

        :schema: BlockDeviceMapping
        '''
        if isinstance(ebs, dict):
            ebs = BlockDeviceMappingEbs(**ebs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1dde2b7b9f057e6a4056311f29fd57ec58a1a8363155c7695fd24057b666b9f)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
            check_type(argname="argument no_device", value=no_device, expected_type=type_hints["no_device"])
            check_type(argname="argument virtual_name", value=virtual_name, expected_type=type_hints["virtual_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_name is not None:
            self._values["device_name"] = device_name
        if ebs is not None:
            self._values["ebs"] = ebs
        if no_device is not None:
            self._values["no_device"] = no_device
        if virtual_name is not None:
            self._values["virtual_name"] = virtual_name

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BlockDeviceMapping#deviceName
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs(self) -> typing.Optional["BlockDeviceMappingEbs"]:
        '''
        :schema: BlockDeviceMapping#ebs
        '''
        result = self._values.get("ebs")
        return typing.cast(typing.Optional["BlockDeviceMappingEbs"], result)

    @builtins.property
    def no_device(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BlockDeviceMapping#noDevice
        '''
        result = self._values.get("no_device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BlockDeviceMapping#virtualName
        '''
        result = self._values.get("virtual_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockDeviceMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.BlockDeviceMappingEbs",
    jsii_struct_bases=[],
    name_mapping={
        "delete_on_termination": "deleteOnTermination",
        "dynamic_volume_size": "dynamicVolumeSize",
        "encrypted": "encrypted",
        "iops": "iops",
        "kms_key_id": "kmsKeyId",
        "snapshot_id": "snapshotId",
        "throughput": "throughput",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class BlockDeviceMappingEbs:
    def __init__(
        self,
        *,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        dynamic_volume_size: typing.Optional[typing.Union["BlockDeviceMappingEbsDynamicVolumeSize", typing.Dict[builtins.str, typing.Any]]] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional["BlockDeviceMappingEbsVolumeType"] = None,
    ) -> None:
        '''
        :param delete_on_termination: 
        :param dynamic_volume_size: 
        :param encrypted: 
        :param iops: 
        :param kms_key_id: 
        :param snapshot_id: 
        :param throughput: 
        :param volume_size: 
        :param volume_type: 

        :schema: BlockDeviceMappingEbs
        '''
        if isinstance(dynamic_volume_size, dict):
            dynamic_volume_size = BlockDeviceMappingEbsDynamicVolumeSize(**dynamic_volume_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c10ac981f599a2044252842b6ffbb099615349100cfb1361cd6e2bdd512022)
            check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
            check_type(argname="argument dynamic_volume_size", value=dynamic_volume_size, expected_type=type_hints["dynamic_volume_size"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if dynamic_volume_size is not None:
            self._values["dynamic_volume_size"] = dynamic_volume_size
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def delete_on_termination(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: BlockDeviceMappingEbs#deleteOnTermination
        '''
        result = self._values.get("delete_on_termination")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dynamic_volume_size(
        self,
    ) -> typing.Optional["BlockDeviceMappingEbsDynamicVolumeSize"]:
        '''
        :schema: BlockDeviceMappingEbs#dynamicVolumeSize
        '''
        result = self._values.get("dynamic_volume_size")
        return typing.cast(typing.Optional["BlockDeviceMappingEbsDynamicVolumeSize"], result)

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: BlockDeviceMappingEbs#encrypted
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: BlockDeviceMappingEbs#iops
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BlockDeviceMappingEbs#kmsKeyId
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BlockDeviceMappingEbs#snapshotId
        '''
        result = self._values.get("snapshot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: BlockDeviceMappingEbs#throughput
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: BlockDeviceMappingEbs#volumeSize
        '''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional["BlockDeviceMappingEbsVolumeType"]:
        '''
        :schema: BlockDeviceMappingEbs#volumeType
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional["BlockDeviceMappingEbsVolumeType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockDeviceMappingEbs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.BlockDeviceMappingEbsDynamicVolumeSize",
    jsii_struct_bases=[],
    name_mapping={
        "base_size": "baseSize",
        "resource": "resource",
        "size_per_resource_unit": "sizePerResourceUnit",
    },
)
class BlockDeviceMappingEbsDynamicVolumeSize:
    def __init__(
        self,
        *,
        base_size: typing.Optional[jsii.Number] = None,
        resource: typing.Optional[builtins.str] = None,
        size_per_resource_unit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_size: 
        :param resource: 
        :param size_per_resource_unit: 

        :schema: BlockDeviceMappingEbsDynamicVolumeSize
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b9b60e72321319ce12124b3d90ceadc1a8e2d7961b00b52512fa9d591f28b5)
            check_type(argname="argument base_size", value=base_size, expected_type=type_hints["base_size"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument size_per_resource_unit", value=size_per_resource_unit, expected_type=type_hints["size_per_resource_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_size is not None:
            self._values["base_size"] = base_size
        if resource is not None:
            self._values["resource"] = resource
        if size_per_resource_unit is not None:
            self._values["size_per_resource_unit"] = size_per_resource_unit

    @builtins.property
    def base_size(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: BlockDeviceMappingEbsDynamicVolumeSize#baseSize
        '''
        result = self._values.get("base_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''
        :schema: BlockDeviceMappingEbsDynamicVolumeSize#resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_per_resource_unit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: BlockDeviceMappingEbsDynamicVolumeSize#sizePerResourceUnit
        '''
        result = self._values.get("size_per_resource_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockDeviceMappingEbsDynamicVolumeSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.BlockDeviceMappingEbsVolumeType"
)
class BlockDeviceMappingEbsVolumeType(enum.Enum):
    '''
    :schema: BlockDeviceMappingEbsVolumeType
    '''

    STANDARD = "STANDARD"
    '''standard.'''
    IO1 = "IO1"
    '''io1.'''
    GP2 = "GP2"
    '''gp2.'''


class CfnGroup(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroup",
):
    '''A CloudFormation ``Spot::Elastigroup::Group``.

    :cloudformationResource: Spot::Elastigroup::Group
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        credentials: typing.Union["CfnGroupPropsCredentials", typing.Dict[builtins.str, typing.Any]],
        group: typing.Optional[typing.Union["CfnGroupPropsGroup", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Spot::Elastigroup::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param credentials: 
        :param group: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e0a0cd3b8949c7f43b677824dc627fa20df44be75a759d4b20a225cc4e0d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(credentials=credentials, group=group)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnGroupProps":
        '''Resource props.'''
        return typing.cast("CfnGroupProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={"credentials": "credentials", "group": "group"},
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        credentials: typing.Union["CfnGroupPropsCredentials", typing.Dict[builtins.str, typing.Any]],
        group: typing.Optional[typing.Union["CfnGroupPropsGroup", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The Spot Elastigroup Resource allows you to create, update, manage, and delete Spot Elastigroups easily with CloudFormation.

        :param credentials: 
        :param group: 

        :schema: CfnGroupProps
        '''
        if isinstance(credentials, dict):
            credentials = CfnGroupPropsCredentials(**credentials)
        if isinstance(group, dict):
            group = CfnGroupPropsGroup(**group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82575e10378d1e80a2be695e0a4451974db65b6b7371f3a9c5206a6ada5b6571)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
        }
        if group is not None:
            self._values["group"] = group

    @builtins.property
    def credentials(self) -> "CfnGroupPropsCredentials":
        '''
        :schema: CfnGroupProps#credentials
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast("CfnGroupPropsCredentials", result)

    @builtins.property
    def group(self) -> typing.Optional["CfnGroupPropsGroup"]:
        '''
        :schema: CfnGroupProps#group
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional["CfnGroupPropsGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsCredentials",
    jsii_struct_bases=[],
    name_mapping={"access_token": "accessToken", "account_id": "accountId"},
)
class CfnGroupPropsCredentials:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: 
        :param account_id: 

        :schema: CfnGroupPropsCredentials
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0c275b3c48a48d155c02caed86b6136e593b75b08a89b188a1b6de40a12bad)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsCredentials#accessToken
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsCredentials#accountId
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroup",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "compute": "compute",
        "created_at": "createdAt",
        "description": "description",
        "group_id": "groupId",
        "name": "name",
        "region": "region",
        "scaling": "scaling",
        "scheduling": "scheduling",
        "strategy": "strategy",
        "third_parties_integration": "thirdPartiesIntegration",
        "updated_at": "updatedAt",
    },
)
class CfnGroupPropsGroup:
    def __init__(
        self,
        *,
        capacity: typing.Optional[typing.Union["CfnGroupPropsGroupCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        compute: typing.Optional[typing.Union["CfnGroupPropsGroupCompute", typing.Dict[builtins.str, typing.Any]]] = None,
        created_at: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CfnGroupPropsGroupScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduling: typing.Optional[typing.Union["CfnGroupPropsGroupScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        strategy: typing.Optional[typing.Union["CfnGroupPropsGroupStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        third_parties_integration: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        updated_at: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capacity: 
        :param compute: 
        :param created_at: 
        :param description: The description of the elastigroup.
        :param group_id: 
        :param name: The name of the elastigroup.
        :param region: 
        :param scaling: 
        :param scheduling: 
        :param strategy: 
        :param third_parties_integration: 
        :param updated_at: 

        :schema: CfnGroupPropsGroup
        '''
        if isinstance(capacity, dict):
            capacity = CfnGroupPropsGroupCapacity(**capacity)
        if isinstance(compute, dict):
            compute = CfnGroupPropsGroupCompute(**compute)
        if isinstance(scaling, dict):
            scaling = CfnGroupPropsGroupScaling(**scaling)
        if isinstance(scheduling, dict):
            scheduling = CfnGroupPropsGroupScheduling(**scheduling)
        if isinstance(strategy, dict):
            strategy = CfnGroupPropsGroupStrategy(**strategy)
        if isinstance(third_parties_integration, dict):
            third_parties_integration = CfnGroupPropsGroupThirdPartiesIntegration(**third_parties_integration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2da0e1ca2dea5cefa49b31a4b41756489368be15ebc8431dd8794b542eff90)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument compute", value=compute, expected_type=type_hints["compute"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
            check_type(argname="argument scheduling", value=scheduling, expected_type=type_hints["scheduling"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument third_parties_integration", value=third_parties_integration, expected_type=type_hints["third_parties_integration"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if compute is not None:
            self._values["compute"] = compute
        if created_at is not None:
            self._values["created_at"] = created_at
        if description is not None:
            self._values["description"] = description
        if group_id is not None:
            self._values["group_id"] = group_id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if scaling is not None:
            self._values["scaling"] = scaling
        if scheduling is not None:
            self._values["scheduling"] = scheduling
        if strategy is not None:
            self._values["strategy"] = strategy
        if third_parties_integration is not None:
            self._values["third_parties_integration"] = third_parties_integration
        if updated_at is not None:
            self._values["updated_at"] = updated_at

    @builtins.property
    def capacity(self) -> typing.Optional["CfnGroupPropsGroupCapacity"]:
        '''
        :schema: CfnGroupPropsGroup#capacity
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional["CfnGroupPropsGroupCapacity"], result)

    @builtins.property
    def compute(self) -> typing.Optional["CfnGroupPropsGroupCompute"]:
        '''
        :schema: CfnGroupPropsGroup#compute
        '''
        result = self._values.get("compute")
        return typing.cast(typing.Optional["CfnGroupPropsGroupCompute"], result)

    @builtins.property
    def created_at(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroup#createdAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the elastigroup.

        :schema: CfnGroupPropsGroup#description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroup#groupId
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the elastigroup.

        :schema: CfnGroupPropsGroup#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroup#region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling(self) -> typing.Optional["CfnGroupPropsGroupScaling"]:
        '''
        :schema: CfnGroupPropsGroup#scaling
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional["CfnGroupPropsGroupScaling"], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["CfnGroupPropsGroupScheduling"]:
        '''
        :schema: CfnGroupPropsGroup#scheduling
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["CfnGroupPropsGroupScheduling"], result)

    @builtins.property
    def strategy(self) -> typing.Optional["CfnGroupPropsGroupStrategy"]:
        '''
        :schema: CfnGroupPropsGroup#strategy
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["CfnGroupPropsGroupStrategy"], result)

    @builtins.property
    def third_parties_integration(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegration"]:
        '''
        :schema: CfnGroupPropsGroup#thirdPartiesIntegration
        '''
        result = self._values.get("third_parties_integration")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegration"], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroup#updatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "maximum": "maximum",
        "minimum": "minimum",
        "target": "target",
        "unit": "unit",
    },
)
class CfnGroupPropsGroupCapacity:
    def __init__(
        self,
        *,
        maximum: typing.Optional[jsii.Number] = None,
        minimum: typing.Optional[jsii.Number] = None,
        target: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum: 
        :param minimum: 
        :param target: 
        :param unit: 

        :schema: CfnGroupPropsGroupCapacity
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894230b9753e3d68cf11052e16e651cb0d621f7121db214f2ed21c08b9080912)
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum
        if target is not None:
            self._values["target"] = target
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def maximum(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupCapacity#maximum
        '''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupCapacity#minimum
        '''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupCapacity#target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupCapacity#unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupCompute",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "ebs_volume_pool": "ebsVolumePool",
        "elastic_ips": "elasticIps",
        "instance_types": "instanceTypes",
        "launch_specification": "launchSpecification",
        "preferred_availability_zones": "preferredAvailabilityZones",
        "private_ips": "privateIps",
        "product": "product",
        "subnet_ids": "subnetIds",
        "volume_attachments": "volumeAttachments",
    },
)
class CfnGroupPropsGroupCompute:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeAvailabilityZones", typing.Dict[builtins.str, typing.Any]]]] = None,
        ebs_volume_pool: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeEbsVolumePool", typing.Dict[builtins.str, typing.Any]]]] = None,
        elastic_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_types: typing.Optional[typing.Union["CfnGroupPropsGroupComputeInstanceTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        launch_specification: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        product: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume_attachments: typing.Optional[typing.Union["CfnGroupPropsGroupComputeVolumeAttachments", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param ebs_volume_pool: 
        :param elastic_ips: 
        :param instance_types: 
        :param launch_specification: 
        :param preferred_availability_zones: 
        :param private_ips: 
        :param product: 
        :param subnet_ids: 
        :param volume_attachments: 

        :schema: CfnGroupPropsGroupCompute
        '''
        if isinstance(instance_types, dict):
            instance_types = CfnGroupPropsGroupComputeInstanceTypes(**instance_types)
        if isinstance(launch_specification, dict):
            launch_specification = CfnGroupPropsGroupComputeLaunchSpecification(**launch_specification)
        if isinstance(volume_attachments, dict):
            volume_attachments = CfnGroupPropsGroupComputeVolumeAttachments(**volume_attachments)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da077a38f05e3993b1b12bb0749e466d5f318dc90e57119b8d468044262f7994)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument ebs_volume_pool", value=ebs_volume_pool, expected_type=type_hints["ebs_volume_pool"])
            check_type(argname="argument elastic_ips", value=elastic_ips, expected_type=type_hints["elastic_ips"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument launch_specification", value=launch_specification, expected_type=type_hints["launch_specification"])
            check_type(argname="argument preferred_availability_zones", value=preferred_availability_zones, expected_type=type_hints["preferred_availability_zones"])
            check_type(argname="argument private_ips", value=private_ips, expected_type=type_hints["private_ips"])
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument volume_attachments", value=volume_attachments, expected_type=type_hints["volume_attachments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if ebs_volume_pool is not None:
            self._values["ebs_volume_pool"] = ebs_volume_pool
        if elastic_ips is not None:
            self._values["elastic_ips"] = elastic_ips
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if launch_specification is not None:
            self._values["launch_specification"] = launch_specification
        if preferred_availability_zones is not None:
            self._values["preferred_availability_zones"] = preferred_availability_zones
        if private_ips is not None:
            self._values["private_ips"] = private_ips
        if product is not None:
            self._values["product"] = product
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if volume_attachments is not None:
            self._values["volume_attachments"] = volume_attachments

    @builtins.property
    def availability_zones(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeAvailabilityZones"]]:
        '''
        :schema: CfnGroupPropsGroupCompute#availabilityZones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeAvailabilityZones"]], result)

    @builtins.property
    def ebs_volume_pool(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeEbsVolumePool"]]:
        '''
        :schema: CfnGroupPropsGroupCompute#ebsVolumePool
        '''
        result = self._values.get("ebs_volume_pool")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeEbsVolumePool"]], result)

    @builtins.property
    def elastic_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupCompute#elasticIps
        '''
        result = self._values.get("elastic_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeInstanceTypes"]:
        '''
        :schema: CfnGroupPropsGroupCompute#instanceTypes
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeInstanceTypes"], result)

    @builtins.property
    def launch_specification(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecification"]:
        '''
        :schema: CfnGroupPropsGroupCompute#launchSpecification
        '''
        result = self._values.get("launch_specification")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecification"], result)

    @builtins.property
    def preferred_availability_zones(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupCompute#preferredAvailabilityZones
        '''
        result = self._values.get("preferred_availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupCompute#privateIps
        '''
        result = self._values.get("private_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def product(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupCompute#product
        '''
        result = self._values.get("product")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupCompute#subnetIds
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def volume_attachments(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeVolumeAttachments"]:
        '''
        :schema: CfnGroupPropsGroupCompute#volumeAttachments
        '''
        result = self._values.get("volume_attachments")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeVolumeAttachments"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupCompute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeAvailabilityZones",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "placement_group_name": "placementGroupName",
        "subnet_id": "subnetId",
        "subnet_ids": "subnetIds",
    },
)
class CfnGroupPropsGroupComputeAvailabilityZones:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        placement_group_name: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: 
        :param placement_group_name: 
        :param subnet_id: 
        :param subnet_ids: 

        :schema: CfnGroupPropsGroupComputeAvailabilityZones
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5d0ec8dfd5c0d0d2321774c8c961748b40c0360c961e6adc738d3f4b6edff7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument placement_group_name", value=placement_group_name, expected_type=type_hints["placement_group_name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if placement_group_name is not None:
            self._values["placement_group_name"] = placement_group_name
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeAvailabilityZones#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def placement_group_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeAvailabilityZones#placementGroupName
        '''
        result = self._values.get("placement_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeAvailabilityZones#subnetId
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeAvailabilityZones#subnetIds
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeAvailabilityZones(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeEbsVolumePool",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "volume_ids": "volumeIds"},
)
class CfnGroupPropsGroupComputeEbsVolumePool:
    def __init__(
        self,
        *,
        device_name: typing.Optional[builtins.str] = None,
        volume_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param device_name: 
        :param volume_ids: 

        :schema: CfnGroupPropsGroupComputeEbsVolumePool
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d595bbc30a37ff454566ec57e1717051bf4b1ef2ef5b8dba29f650a37337c672)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument volume_ids", value=volume_ids, expected_type=type_hints["volume_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_name is not None:
            self._values["device_name"] = device_name
        if volume_ids is not None:
            self._values["volume_ids"] = volume_ids

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeEbsVolumePool#deviceName
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeEbsVolumePool#volumeIds
        '''
        result = self._values.get("volume_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeEbsVolumePool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeInstanceTypes",
    jsii_struct_bases=[],
    name_mapping={
        "on_demand": "onDemand",
        "on_demand_types": "onDemandTypes",
        "preferred_spot": "preferredSpot",
        "resource_requirements": "resourceRequirements",
        "spot": "spot",
        "weights": "weights",
    },
)
class CfnGroupPropsGroupComputeInstanceTypes:
    def __init__(
        self,
        *,
        on_demand: typing.Optional[builtins.str] = None,
        on_demand_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_spot: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_requirements: typing.Optional[typing.Union["CfnGroupPropsGroupComputeInstanceTypesResourceRequirements", typing.Dict[builtins.str, typing.Any]]] = None,
        spot: typing.Optional[typing.Sequence[builtins.str]] = None,
        weights: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeInstanceTypesWeights", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param on_demand: 
        :param on_demand_types: 
        :param preferred_spot: 
        :param resource_requirements: 
        :param spot: 
        :param weights: 

        :schema: CfnGroupPropsGroupComputeInstanceTypes
        '''
        if isinstance(resource_requirements, dict):
            resource_requirements = CfnGroupPropsGroupComputeInstanceTypesResourceRequirements(**resource_requirements)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1927a0c9607121c4d10644386828ab615815e17301dd36b4b7478e6b8f2c41c5)
            check_type(argname="argument on_demand", value=on_demand, expected_type=type_hints["on_demand"])
            check_type(argname="argument on_demand_types", value=on_demand_types, expected_type=type_hints["on_demand_types"])
            check_type(argname="argument preferred_spot", value=preferred_spot, expected_type=type_hints["preferred_spot"])
            check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument weights", value=weights, expected_type=type_hints["weights"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_demand is not None:
            self._values["on_demand"] = on_demand
        if on_demand_types is not None:
            self._values["on_demand_types"] = on_demand_types
        if preferred_spot is not None:
            self._values["preferred_spot"] = preferred_spot
        if resource_requirements is not None:
            self._values["resource_requirements"] = resource_requirements
        if spot is not None:
            self._values["spot"] = spot
        if weights is not None:
            self._values["weights"] = weights

    @builtins.property
    def on_demand(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypes#onDemand
        '''
        result = self._values.get("on_demand")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypes#onDemandTypes
        '''
        result = self._values.get("on_demand_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_spot(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypes#preferredSpot
        '''
        result = self._values.get("preferred_spot")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_requirements(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeInstanceTypesResourceRequirements"]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypes#resourceRequirements
        '''
        result = self._values.get("resource_requirements")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeInstanceTypesResourceRequirements"], result)

    @builtins.property
    def spot(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypes#spot
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weights(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeInstanceTypesWeights"]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypes#weights
        '''
        result = self._values.get("weights")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeInstanceTypesWeights"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeInstanceTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeInstanceTypesResourceRequirements",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_instance_families": "excludedInstanceFamilies",
        "excluded_instance_generations": "excludedInstanceGenerations",
        "excluded_instance_types": "excludedInstanceTypes",
        "required_gpu": "requiredGpu",
        "required_memory": "requiredMemory",
        "required_v_cpu": "requiredVCpu",
    },
)
class CfnGroupPropsGroupComputeInstanceTypesResourceRequirements:
    def __init__(
        self,
        *,
        excluded_instance_families: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_gpu: typing.Optional[typing.Union["ResourceRequirement", typing.Dict[builtins.str, typing.Any]]] = None,
        required_memory: typing.Optional[typing.Union["ResourceRequirement", typing.Dict[builtins.str, typing.Any]]] = None,
        required_v_cpu: typing.Optional[typing.Union["ResourceRequirement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_instance_families: 
        :param excluded_instance_generations: 
        :param excluded_instance_types: 
        :param required_gpu: 
        :param required_memory: 
        :param required_v_cpu: 

        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements
        '''
        if isinstance(required_gpu, dict):
            required_gpu = ResourceRequirement(**required_gpu)
        if isinstance(required_memory, dict):
            required_memory = ResourceRequirement(**required_memory)
        if isinstance(required_v_cpu, dict):
            required_v_cpu = ResourceRequirement(**required_v_cpu)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36d674982e3043c79c6f1ceef49201554fb37010c8ec36445cd8338b1ed5743)
            check_type(argname="argument excluded_instance_families", value=excluded_instance_families, expected_type=type_hints["excluded_instance_families"])
            check_type(argname="argument excluded_instance_generations", value=excluded_instance_generations, expected_type=type_hints["excluded_instance_generations"])
            check_type(argname="argument excluded_instance_types", value=excluded_instance_types, expected_type=type_hints["excluded_instance_types"])
            check_type(argname="argument required_gpu", value=required_gpu, expected_type=type_hints["required_gpu"])
            check_type(argname="argument required_memory", value=required_memory, expected_type=type_hints["required_memory"])
            check_type(argname="argument required_v_cpu", value=required_v_cpu, expected_type=type_hints["required_v_cpu"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_instance_families is not None:
            self._values["excluded_instance_families"] = excluded_instance_families
        if excluded_instance_generations is not None:
            self._values["excluded_instance_generations"] = excluded_instance_generations
        if excluded_instance_types is not None:
            self._values["excluded_instance_types"] = excluded_instance_types
        if required_gpu is not None:
            self._values["required_gpu"] = required_gpu
        if required_memory is not None:
            self._values["required_memory"] = required_memory
        if required_v_cpu is not None:
            self._values["required_v_cpu"] = required_v_cpu

    @builtins.property
    def excluded_instance_families(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements#excludedInstanceFamilies
        '''
        result = self._values.get("excluded_instance_families")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_instance_generations(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements#excludedInstanceGenerations
        '''
        result = self._values.get("excluded_instance_generations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements#excludedInstanceTypes
        '''
        result = self._values.get("excluded_instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required_gpu(self) -> typing.Optional["ResourceRequirement"]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements#requiredGpu
        '''
        result = self._values.get("required_gpu")
        return typing.cast(typing.Optional["ResourceRequirement"], result)

    @builtins.property
    def required_memory(self) -> typing.Optional["ResourceRequirement"]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements#requiredMemory
        '''
        result = self._values.get("required_memory")
        return typing.cast(typing.Optional["ResourceRequirement"], result)

    @builtins.property
    def required_v_cpu(self) -> typing.Optional["ResourceRequirement"]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesResourceRequirements#requiredVCpu
        '''
        result = self._values.get("required_v_cpu")
        return typing.cast(typing.Optional["ResourceRequirement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeInstanceTypesResourceRequirements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeInstanceTypesWeights",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "weighted_capacity": "weightedCapacity",
    },
)
class CfnGroupPropsGroupComputeInstanceTypesWeights:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        weighted_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_type: 
        :param weighted_capacity: 

        :schema: CfnGroupPropsGroupComputeInstanceTypesWeights
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e79661dd516b26fbee632de105989cfc60917b924e8957e9c70d547c3e174ee)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument weighted_capacity", value=weighted_capacity, expected_type=type_hints["weighted_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if weighted_capacity is not None:
            self._values["weighted_capacity"] = weighted_capacity

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesWeights#instanceType
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weighted_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeInstanceTypesWeights#weightedCapacity
        '''
        result = self._values.get("weighted_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeInstanceTypesWeights(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecification",
    jsii_struct_bases=[],
    name_mapping={
        "auto_healing": "autoHealing",
        "block_device_mappings": "blockDeviceMappings",
        "cpu_options": "cpuOptions",
        "credit_specification": "creditSpecification",
        "ebs_optimized": "ebsOptimized",
        "health_check_grace_period": "healthCheckGracePeriod",
        "health_check_type": "healthCheckType",
        "health_check_unhealthy_duration_before_replacement": "healthCheckUnhealthyDurationBeforeReplacement",
        "iam_role": "iamRole",
        "image_id": "imageId",
        "images": "images",
        "itf": "itf",
        "key_pair": "keyPair",
        "load_balancer_name": "loadBalancerName",
        "load_balancer_names": "loadBalancerNames",
        "load_balancers_config": "loadBalancersConfig",
        "metadata_options": "metadataOptions",
        "monitoring": "monitoring",
        "network_interfaces": "networkInterfaces",
        "resource_tag_specification": "resourceTagSpecification",
        "security_group_ids": "securityGroupIds",
        "shutdown_script": "shutdownScript",
        "tags": "tags",
        "tenancy": "tenancy",
        "user_data": "userData",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecification:
    def __init__(
        self,
        *,
        auto_healing: typing.Optional[builtins.bool] = None,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[BlockDeviceMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
        cpu_options: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        credit_specification: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_optimized: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[jsii.Number] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        health_check_unhealthy_duration_before_replacement: typing.Optional[jsii.Number] = None,
        iam_role: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationIamRole", typing.Dict[builtins.str, typing.Any]]] = None,
        image_id: typing.Optional[builtins.str] = None,
        images: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationImages", typing.Dict[builtins.str, typing.Any]]]] = None,
        itf: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItf", typing.Dict[builtins.str, typing.Any]]] = None,
        key_pair: typing.Optional[builtins.str] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        load_balancer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        load_balancers_config: typing.Optional[typing.Union["LoadBalancersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata_options: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[builtins.bool] = None,
        network_interfaces: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_tag_specification: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        shutdown_script: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        tenancy: typing.Optional[builtins.str] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_healing: 
        :param block_device_mappings: 
        :param cpu_options: 
        :param credit_specification: 
        :param ebs_optimized: 
        :param health_check_grace_period: 
        :param health_check_type: 
        :param health_check_unhealthy_duration_before_replacement: 
        :param iam_role: 
        :param image_id: 
        :param images: 
        :param itf: 
        :param key_pair: 
        :param load_balancer_name: 
        :param load_balancer_names: 
        :param load_balancers_config: 
        :param metadata_options: 
        :param monitoring: 
        :param network_interfaces: 
        :param resource_tag_specification: 
        :param security_group_ids: 
        :param shutdown_script: 
        :param tags: 
        :param tenancy: 
        :param user_data: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecification
        '''
        if isinstance(cpu_options, dict):
            cpu_options = CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions(**cpu_options)
        if isinstance(credit_specification, dict):
            credit_specification = CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification(**credit_specification)
        if isinstance(iam_role, dict):
            iam_role = CfnGroupPropsGroupComputeLaunchSpecificationIamRole(**iam_role)
        if isinstance(itf, dict):
            itf = CfnGroupPropsGroupComputeLaunchSpecificationItf(**itf)
        if isinstance(load_balancers_config, dict):
            load_balancers_config = LoadBalancersConfig(**load_balancers_config)
        if isinstance(metadata_options, dict):
            metadata_options = CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions(**metadata_options)
        if isinstance(resource_tag_specification, dict):
            resource_tag_specification = CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification(**resource_tag_specification)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eee7380e54403b9ce880f4d67b7075395a3a7149abf51a88f9e1a9e846bc266)
            check_type(argname="argument auto_healing", value=auto_healing, expected_type=type_hints["auto_healing"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument cpu_options", value=cpu_options, expected_type=type_hints["cpu_options"])
            check_type(argname="argument credit_specification", value=credit_specification, expected_type=type_hints["credit_specification"])
            check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument health_check_type", value=health_check_type, expected_type=type_hints["health_check_type"])
            check_type(argname="argument health_check_unhealthy_duration_before_replacement", value=health_check_unhealthy_duration_before_replacement, expected_type=type_hints["health_check_unhealthy_duration_before_replacement"])
            check_type(argname="argument iam_role", value=iam_role, expected_type=type_hints["iam_role"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument itf", value=itf, expected_type=type_hints["itf"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument load_balancer_names", value=load_balancer_names, expected_type=type_hints["load_balancer_names"])
            check_type(argname="argument load_balancers_config", value=load_balancers_config, expected_type=type_hints["load_balancers_config"])
            check_type(argname="argument metadata_options", value=metadata_options, expected_type=type_hints["metadata_options"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument resource_tag_specification", value=resource_tag_specification, expected_type=type_hints["resource_tag_specification"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument shutdown_script", value=shutdown_script, expected_type=type_hints["shutdown_script"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_healing is not None:
            self._values["auto_healing"] = auto_healing
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if cpu_options is not None:
            self._values["cpu_options"] = cpu_options
        if credit_specification is not None:
            self._values["credit_specification"] = credit_specification
        if ebs_optimized is not None:
            self._values["ebs_optimized"] = ebs_optimized
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if health_check_type is not None:
            self._values["health_check_type"] = health_check_type
        if health_check_unhealthy_duration_before_replacement is not None:
            self._values["health_check_unhealthy_duration_before_replacement"] = health_check_unhealthy_duration_before_replacement
        if iam_role is not None:
            self._values["iam_role"] = iam_role
        if image_id is not None:
            self._values["image_id"] = image_id
        if images is not None:
            self._values["images"] = images
        if itf is not None:
            self._values["itf"] = itf
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if load_balancer_names is not None:
            self._values["load_balancer_names"] = load_balancer_names
        if load_balancers_config is not None:
            self._values["load_balancers_config"] = load_balancers_config
        if metadata_options is not None:
            self._values["metadata_options"] = metadata_options
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces
        if resource_tag_specification is not None:
            self._values["resource_tag_specification"] = resource_tag_specification
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if shutdown_script is not None:
            self._values["shutdown_script"] = shutdown_script
        if tags is not None:
            self._values["tags"] = tags
        if tenancy is not None:
            self._values["tenancy"] = tenancy
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def auto_healing(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#autoHealing
        '''
        result = self._values.get("auto_healing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def block_device_mappings(self) -> typing.Optional[typing.List[BlockDeviceMapping]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#blockDeviceMappings
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.List[BlockDeviceMapping]], result)

    @builtins.property
    def cpu_options(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#cpuOptions
        '''
        result = self._values.get("cpu_options")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions"], result)

    @builtins.property
    def credit_specification(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#creditSpecification
        '''
        result = self._values.get("credit_specification")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification"], result)

    @builtins.property
    def ebs_optimized(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#ebsOptimized
        '''
        result = self._values.get("ebs_optimized")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#healthCheckGracePeriod
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#healthCheckType
        '''
        result = self._values.get("health_check_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_unhealthy_duration_before_replacement(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#healthCheckUnhealthyDurationBeforeReplacement
        '''
        result = self._values.get("health_check_unhealthy_duration_before_replacement")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def iam_role(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationIamRole"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#iamRole
        '''
        result = self._values.get("iam_role")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationIamRole"], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#imageId
        '''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def images(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationImages"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#images
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationImages"]], result)

    @builtins.property
    def itf(self) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationItf"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#itf
        '''
        result = self._values.get("itf")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationItf"], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#keyPair
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#loadBalancerName
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#loadBalancerNames
        '''
        result = self._values.get("load_balancer_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def load_balancers_config(self) -> typing.Optional["LoadBalancersConfig"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#loadBalancersConfig
        '''
        result = self._values.get("load_balancers_config")
        return typing.cast(typing.Optional["LoadBalancersConfig"], result)

    @builtins.property
    def metadata_options(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#metadataOptions
        '''
        result = self._values.get("metadata_options")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions"], result)

    @builtins.property
    def monitoring(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#monitoring
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#networkInterfaces
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces"]], result)

    @builtins.property
    def resource_tag_specification(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#resourceTagSpecification
        '''
        result = self._values.get("resource_tag_specification")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification"], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#securityGroupIds
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shutdown_script(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#shutdownScript
        '''
        result = self._values.get("shutdown_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#tenancy
        '''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecification#userData
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions",
    jsii_struct_bases=[],
    name_mapping={"threads_per_core": "threadsPerCore"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions:
    def __init__(
        self,
        *,
        threads_per_core: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param threads_per_core: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb835b550016d6f85ff299683788b082d41d5acb85f3e613f39b5dd648d2c6d)
            check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if threads_per_core is not None:
            self._values["threads_per_core"] = threads_per_core

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions#threadsPerCore
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification",
    jsii_struct_bases=[],
    name_mapping={"cpu_credits": "cpuCredits"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification:
    def __init__(self, *, cpu_credits: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cpu_credits: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aaa874b619453995216e0ab10da8f9687217431dcb5d0d3957bef2dda4a73b0)
            check_type(argname="argument cpu_credits", value=cpu_credits, expected_type=type_hints["cpu_credits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_credits is not None:
            self._values["cpu_credits"] = cpu_credits

    @builtins.property
    def cpu_credits(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification#cpuCredits
        '''
        result = self._values.get("cpu_credits")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationIamRole",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "name": "name"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationIamRole:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: 
        :param name: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationIamRole
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aca8cb410a3729539a4a314dbce75c50198f529ee196a1999bc9f9ca52c6be1)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationIamRole#arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationIamRole#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationIamRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationImages",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationImages:
    def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param id: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationImages
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d3299795f9fcec237855c957088013fbee6c78c61a938a457a31c9e0ccb6bd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationImages#id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItf",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_target_groups": "fixedTargetGroups",
        "load_balancers": "loadBalancers",
        "migration_healthiness_threshold": "migrationHealthinessThreshold",
        "target_group_config": "targetGroupConfig",
        "weight_strategy": "weightStrategy",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecificationItf:
    def __init__(
        self,
        *,
        fixed_target_groups: typing.Optional[builtins.bool] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers", typing.Dict[builtins.str, typing.Any]]]] = None,
        migration_healthiness_threshold: typing.Optional[jsii.Number] = None,
        target_group_config: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        weight_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fixed_target_groups: 
        :param load_balancers: 
        :param migration_healthiness_threshold: 
        :param target_group_config: 
        :param weight_strategy: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItf
        '''
        if isinstance(target_group_config, dict):
            target_group_config = CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig(**target_group_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755e4bc12352443d3bf7d30e63693ab166a298dcf9df4b22a4bee336329636ce)
            check_type(argname="argument fixed_target_groups", value=fixed_target_groups, expected_type=type_hints["fixed_target_groups"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument migration_healthiness_threshold", value=migration_healthiness_threshold, expected_type=type_hints["migration_healthiness_threshold"])
            check_type(argname="argument target_group_config", value=target_group_config, expected_type=type_hints["target_group_config"])
            check_type(argname="argument weight_strategy", value=weight_strategy, expected_type=type_hints["weight_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed_target_groups is not None:
            self._values["fixed_target_groups"] = fixed_target_groups
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if migration_healthiness_threshold is not None:
            self._values["migration_healthiness_threshold"] = migration_healthiness_threshold
        if target_group_config is not None:
            self._values["target_group_config"] = target_group_config
        if weight_strategy is not None:
            self._values["weight_strategy"] = weight_strategy

    @builtins.property
    def fixed_target_groups(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItf#fixedTargetGroups
        '''
        result = self._values.get("fixed_target_groups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancers(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItf#loadBalancers
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers"]], result)

    @builtins.property
    def migration_healthiness_threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItf#migrationHealthinessThreshold
        '''
        result = self._values.get("migration_healthiness_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_group_config(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItf#targetGroupConfig
        '''
        result = self._values.get("target_group_config")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig"], result)

    @builtins.property
    def weight_strategy(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItf#weightStrategy
        '''
        result = self._values.get("weight_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "default_static_target_groups": "defaultStaticTargetGroups",
        "listener_rules": "listenerRules",
        "load_balancer_arn": "loadBalancerArn",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers:
    def __init__(
        self,
        *,
        default_static_target_groups: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups", typing.Dict[builtins.str, typing.Any]]]] = None,
        listener_rules: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules", typing.Dict[builtins.str, typing.Any]]]] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_static_target_groups: 
        :param listener_rules: 
        :param load_balancer_arn: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da34d258e3d231f155198dc801d0e0e7b0d74a701b7bdaebec2583d6b1744e9)
            check_type(argname="argument default_static_target_groups", value=default_static_target_groups, expected_type=type_hints["default_static_target_groups"])
            check_type(argname="argument listener_rules", value=listener_rules, expected_type=type_hints["listener_rules"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_static_target_groups is not None:
            self._values["default_static_target_groups"] = default_static_target_groups
        if listener_rules is not None:
            self._values["listener_rules"] = listener_rules
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn

    @builtins.property
    def default_static_target_groups(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers#defaultStaticTargetGroups
        '''
        result = self._values.get("default_static_target_groups")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups"]], result)

    @builtins.property
    def listener_rules(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers#listenerRules
        '''
        result = self._values.get("listener_rules")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules"]], result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers#loadBalancerArn
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "percentage": "percentage"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param arn: 
        :param percentage: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3484dacc0debdccf903c8b49867491c27b66ef678a67bfab25c49a0fdf7b1ba)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups#arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups#percentage
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules",
    jsii_struct_bases=[],
    name_mapping={"rule_arn": "ruleArn", "static_target_groups": "staticTargetGroups"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules:
    def __init__(
        self,
        *,
        rule_arn: typing.Optional[builtins.str] = None,
        static_target_groups: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param rule_arn: 
        :param static_target_groups: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02be5086ed9796560b802f79651646b6581bef0468fbdabae12b2f4f09e00daf)
            check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
            check_type(argname="argument static_target_groups", value=static_target_groups, expected_type=type_hints["static_target_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_arn is not None:
            self._values["rule_arn"] = rule_arn
        if static_target_groups is not None:
            self._values["static_target_groups"] = static_target_groups

    @builtins.property
    def rule_arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules#ruleArn
        '''
        result = self._values.get("rule_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_target_groups(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules#staticTargetGroups
        '''
        result = self._values.get("static_target_groups")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "percentage": "percentage"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param arn: 
        :param percentage: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e67bacc6146f93adb7153121dd549336b5b85e3fcadd270994cda590b60d1b)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups#arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups#percentage
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
        "healthy_threshold_count": "healthyThresholdCount",
        "matcher": "matcher",
        "port": "port",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "tags": "tags",
        "unhealthy_threshold_count": "unhealthyThresholdCount",
        "vpc_id": "vpcId",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig:
    def __init__(
        self,
        *,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[builtins.str] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        matcher: typing.Optional[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param health_check_interval_seconds: 
        :param health_check_path: 
        :param health_check_port: 
        :param health_check_protocol: 
        :param health_check_timeout_seconds: 
        :param healthy_threshold_count: 
        :param matcher: 
        :param port: 
        :param protocol: 
        :param protocol_version: 
        :param tags: 
        :param unhealthy_threshold_count: 
        :param vpc_id: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig
        '''
        if isinstance(matcher, dict):
            matcher = CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher(**matcher)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cddfa8eebc74f96bc1d30574ec0f3e129eaf92f0d0a0114c225577edcd2b547)
            check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument health_check_port", value=health_check_port, expected_type=type_hints["health_check_port"])
            check_type(argname="argument health_check_protocol", value=health_check_protocol, expected_type=type_hints["health_check_protocol"])
            check_type(argname="argument health_check_timeout_seconds", value=health_check_timeout_seconds, expected_type=type_hints["health_check_timeout_seconds"])
            check_type(argname="argument healthy_threshold_count", value=healthy_threshold_count, expected_type=type_hints["healthy_threshold_count"])
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument unhealthy_threshold_count", value=unhealthy_threshold_count, expected_type=type_hints["unhealthy_threshold_count"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if health_check_timeout_seconds is not None:
            self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
        if healthy_threshold_count is not None:
            self._values["healthy_threshold_count"] = healthy_threshold_count
        if matcher is not None:
            self._values["matcher"] = matcher
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if tags is not None:
            self._values["tags"] = tags
        if unhealthy_threshold_count is not None:
            self._values["unhealthy_threshold_count"] = unhealthy_threshold_count
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#healthCheckIntervalSeconds
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#healthCheckPath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#healthCheckPort
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#healthCheckProtocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#healthCheckTimeoutSeconds
        '''
        result = self._values.get("health_check_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#healthyThresholdCount
        '''
        result = self._values.get("healthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def matcher(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#matcher
        '''
        result = self._values.get("matcher")
        return typing.cast(typing.Optional["CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#protocolVersion
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#unhealthyThresholdCount
        '''
        result = self._values.get("unhealthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig#vpcId
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher",
    jsii_struct_bases=[],
    name_mapping={"grpc_code": "grpcCode", "http_code": "httpCode"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher:
    def __init__(
        self,
        *,
        grpc_code: typing.Optional[builtins.str] = None,
        http_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_code: 
        :param http_code: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd96ef5b5f304f7cd57803c659afe1a5db8d6553f6e3600e6d48f2c4eeaa6f4)
            check_type(argname="argument grpc_code", value=grpc_code, expected_type=type_hints["grpc_code"])
            check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc_code is not None:
            self._values["grpc_code"] = grpc_code
        if http_code is not None:
            self._values["http_code"] = http_code

    @builtins.property
    def grpc_code(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher#grpcCode
        '''
        result = self._values.get("grpc_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_code(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher#httpCode
        '''
        result = self._values.get("http_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions",
    jsii_struct_bases=[],
    name_mapping={
        "http_put_response_hop_limit": "httpPutResponseHopLimit",
        "http_tokens": "httpTokens",
        "instance_metadata_tags": "instanceMetadataTags",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions:
    def __init__(
        self,
        *,
        http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        http_tokens: typing.Optional[builtins.str] = None,
        instance_metadata_tags: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_put_response_hop_limit: 
        :param http_tokens: 
        :param instance_metadata_tags: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248f070286d3763d0f0acb05a72a7684ebdd247f462aa510288dd92b22cab5fb)
            check_type(argname="argument http_put_response_hop_limit", value=http_put_response_hop_limit, expected_type=type_hints["http_put_response_hop_limit"])
            check_type(argname="argument http_tokens", value=http_tokens, expected_type=type_hints["http_tokens"])
            check_type(argname="argument instance_metadata_tags", value=instance_metadata_tags, expected_type=type_hints["instance_metadata_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_put_response_hop_limit is not None:
            self._values["http_put_response_hop_limit"] = http_put_response_hop_limit
        if http_tokens is not None:
            self._values["http_tokens"] = http_tokens
        if instance_metadata_tags is not None:
            self._values["instance_metadata_tags"] = instance_metadata_tags

    @builtins.property
    def http_put_response_hop_limit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions#httpPutResponseHopLimit
        '''
        result = self._values.get("http_put_response_hop_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_tokens(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions#httpTokens
        '''
        result = self._values.get("http_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_metadata_tags(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions#instanceMetadataTags
        '''
        result = self._values.get("instance_metadata_tags")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={
        "associate_ipv6_address": "associateIpv6Address",
        "associate_public_ip_address": "associatePublicIpAddress",
        "delete_on_termination": "deleteOnTermination",
        "description": "description",
        "device_index": "deviceIndex",
        "groups": "groups",
        "network_interface_id": "networkInterfaceId",
        "private_ip_address": "privateIpAddress",
        "private_ip_addresses": "privateIpAddresses",
        "secondary_private_ip_address_count": "secondaryPrivateIpAddressCount",
        "subnet_id": "subnetId",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces:
    def __init__(
        self,
        *,
        associate_ipv6_address: typing.Optional[builtins.bool] = None,
        associate_public_ip_address: typing.Optional[builtins.bool] = None,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        device_index: typing.Optional[jsii.Number] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_interface_id: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        private_ip_addresses: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses", typing.Dict[builtins.str, typing.Any]]]] = None,
        secondary_private_ip_address_count: typing.Optional[jsii.Number] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param associate_ipv6_address: 
        :param associate_public_ip_address: 
        :param delete_on_termination: 
        :param description: 
        :param device_index: 
        :param groups: 
        :param network_interface_id: 
        :param private_ip_address: 
        :param private_ip_addresses: 
        :param secondary_private_ip_address_count: 
        :param subnet_id: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce5482d06528a4cfa6e3e0d548e8ce44c6c6c3b600486889b2ed9e4a94d8c33)
            check_type(argname="argument associate_ipv6_address", value=associate_ipv6_address, expected_type=type_hints["associate_ipv6_address"])
            check_type(argname="argument associate_public_ip_address", value=associate_public_ip_address, expected_type=type_hints["associate_public_ip_address"])
            check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument device_index", value=device_index, expected_type=type_hints["device_index"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument private_ip_addresses", value=private_ip_addresses, expected_type=type_hints["private_ip_addresses"])
            check_type(argname="argument secondary_private_ip_address_count", value=secondary_private_ip_address_count, expected_type=type_hints["secondary_private_ip_address_count"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associate_ipv6_address is not None:
            self._values["associate_ipv6_address"] = associate_ipv6_address
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if description is not None:
            self._values["description"] = description
        if device_index is not None:
            self._values["device_index"] = device_index
        if groups is not None:
            self._values["groups"] = groups
        if network_interface_id is not None:
            self._values["network_interface_id"] = network_interface_id
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if private_ip_addresses is not None:
            self._values["private_ip_addresses"] = private_ip_addresses
        if secondary_private_ip_address_count is not None:
            self._values["secondary_private_ip_address_count"] = secondary_private_ip_address_count
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def associate_ipv6_address(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#associateIpv6Address
        '''
        result = self._values.get("associate_ipv6_address")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#associatePublicIpAddress
        '''
        result = self._values.get("associate_public_ip_address")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delete_on_termination(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#deleteOnTermination
        '''
        result = self._values.get("delete_on_termination")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_index(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#deviceIndex
        '''
        result = self._values.get("device_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_interface_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#networkInterfaceId
        '''
        result = self._values.get("network_interface_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#privateIpAddress
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_addresses(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses"]]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#privateIpAddresses
        '''
        result = self._values.get("private_ip_addresses")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses"]], result)

    @builtins.property
    def secondary_private_ip_address_count(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#secondaryPrivateIpAddressCount
        '''
        result = self._values.get("secondary_private_ip_address_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces#subnetId
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses",
    jsii_struct_bases=[],
    name_mapping={"primary": "primary", "private_ip_address": "privateIpAddress"},
)
class CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses:
    def __init__(
        self,
        *,
        primary: typing.Optional[builtins.bool] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param primary: 
        :param private_ip_address: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b572230f72340b340b156d8cca3073db997c155a9219e03ee56b5f53e2b0cba8)
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if primary is not None:
            self._values["primary"] = primary
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address

    @builtins.property
    def primary(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses#primary
        '''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses#privateIpAddress
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification",
    jsii_struct_bases=[],
    name_mapping={
        "amis": "amis",
        "enis": "enis",
        "snapshots": "snapshots",
        "volumes": "volumes",
    },
)
class CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification:
    def __init__(
        self,
        *,
        amis: typing.Optional[typing.Union["ResourceTagSpecificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enis: typing.Optional[typing.Union["ResourceTagSpecificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshots: typing.Optional[typing.Union["ResourceTagSpecificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[typing.Union["ResourceTagSpecificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amis: 
        :param enis: 
        :param snapshots: 
        :param volumes: 

        :schema: CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification
        '''
        if isinstance(amis, dict):
            amis = ResourceTagSpecificationConfig(**amis)
        if isinstance(enis, dict):
            enis = ResourceTagSpecificationConfig(**enis)
        if isinstance(snapshots, dict):
            snapshots = ResourceTagSpecificationConfig(**snapshots)
        if isinstance(volumes, dict):
            volumes = ResourceTagSpecificationConfig(**volumes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486bebec6c5f0f761ff3d18d12926295a9cddccfe34e63af6eb26a0608458f4f)
            check_type(argname="argument amis", value=amis, expected_type=type_hints["amis"])
            check_type(argname="argument enis", value=enis, expected_type=type_hints["enis"])
            check_type(argname="argument snapshots", value=snapshots, expected_type=type_hints["snapshots"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amis is not None:
            self._values["amis"] = amis
        if enis is not None:
            self._values["enis"] = enis
        if snapshots is not None:
            self._values["snapshots"] = snapshots
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def amis(self) -> typing.Optional["ResourceTagSpecificationConfig"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification#amis
        '''
        result = self._values.get("amis")
        return typing.cast(typing.Optional["ResourceTagSpecificationConfig"], result)

    @builtins.property
    def enis(self) -> typing.Optional["ResourceTagSpecificationConfig"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification#enis
        '''
        result = self._values.get("enis")
        return typing.cast(typing.Optional["ResourceTagSpecificationConfig"], result)

    @builtins.property
    def snapshots(self) -> typing.Optional["ResourceTagSpecificationConfig"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification#snapshots
        '''
        result = self._values.get("snapshots")
        return typing.cast(typing.Optional["ResourceTagSpecificationConfig"], result)

    @builtins.property
    def volumes(self) -> typing.Optional["ResourceTagSpecificationConfig"]:
        '''
        :schema: CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification#volumes
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional["ResourceTagSpecificationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeVolumeAttachments",
    jsii_struct_bases=[],
    name_mapping={"volumes": "volumes"},
)
class CfnGroupPropsGroupComputeVolumeAttachments:
    def __init__(
        self,
        *,
        volumes: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupComputeVolumeAttachmentsVolumes", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param volumes: 

        :schema: CfnGroupPropsGroupComputeVolumeAttachments
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db4a1b4732e973cec3c4efa25eb7a533b3368e4e6ccda3f84131673be460955)
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupComputeVolumeAttachmentsVolumes"]]:
        '''
        :schema: CfnGroupPropsGroupComputeVolumeAttachments#volumes
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupComputeVolumeAttachmentsVolumes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeVolumeAttachments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupComputeVolumeAttachmentsVolumes",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "volume_id": "volumeId"},
)
class CfnGroupPropsGroupComputeVolumeAttachmentsVolumes:
    def __init__(
        self,
        *,
        device_name: typing.Optional[builtins.str] = None,
        volume_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: 
        :param volume_id: 

        :schema: CfnGroupPropsGroupComputeVolumeAttachmentsVolumes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc60095e42a0f481392dc4e1a9ca724c35a1f20cf970c053ab78ed058810d67)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_name is not None:
            self._values["device_name"] = device_name
        if volume_id is not None:
            self._values["volume_id"] = volume_id

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeVolumeAttachmentsVolumes#deviceName
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupComputeVolumeAttachmentsVolumes#volumeId
        '''
        result = self._values.get("volume_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupComputeVolumeAttachmentsVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupScaling",
    jsii_struct_bases=[],
    name_mapping={
        "down": "down",
        "multiple_metrics": "multipleMetrics",
        "target": "target",
        "up": "up",
    },
)
class CfnGroupPropsGroupScaling:
    def __init__(
        self,
        *,
        down: typing.Optional[typing.Sequence[typing.Union["ScalingDownPolicy", typing.Dict[builtins.str, typing.Any]]]] = None,
        multiple_metrics: typing.Optional[typing.Union["CfnGroupPropsGroupScalingMultipleMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Sequence[typing.Union["ScalingTargetPolicy", typing.Dict[builtins.str, typing.Any]]]] = None,
        up: typing.Optional[typing.Sequence[typing.Union["ScalingUpPolicy", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param down: 
        :param multiple_metrics: 
        :param target: 
        :param up: 

        :schema: CfnGroupPropsGroupScaling
        '''
        if isinstance(multiple_metrics, dict):
            multiple_metrics = CfnGroupPropsGroupScalingMultipleMetrics(**multiple_metrics)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e7511661618b1dbaa7841f92e9a1536c3d91439dc5014d69abc3c56f74b20a)
            check_type(argname="argument down", value=down, expected_type=type_hints["down"])
            check_type(argname="argument multiple_metrics", value=multiple_metrics, expected_type=type_hints["multiple_metrics"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument up", value=up, expected_type=type_hints["up"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if down is not None:
            self._values["down"] = down
        if multiple_metrics is not None:
            self._values["multiple_metrics"] = multiple_metrics
        if target is not None:
            self._values["target"] = target
        if up is not None:
            self._values["up"] = up

    @builtins.property
    def down(self) -> typing.Optional[typing.List["ScalingDownPolicy"]]:
        '''
        :schema: CfnGroupPropsGroupScaling#down
        '''
        result = self._values.get("down")
        return typing.cast(typing.Optional[typing.List["ScalingDownPolicy"]], result)

    @builtins.property
    def multiple_metrics(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupScalingMultipleMetrics"]:
        '''
        :schema: CfnGroupPropsGroupScaling#multipleMetrics
        '''
        result = self._values.get("multiple_metrics")
        return typing.cast(typing.Optional["CfnGroupPropsGroupScalingMultipleMetrics"], result)

    @builtins.property
    def target(self) -> typing.Optional[typing.List["ScalingTargetPolicy"]]:
        '''
        :schema: CfnGroupPropsGroupScaling#target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.List["ScalingTargetPolicy"]], result)

    @builtins.property
    def up(self) -> typing.Optional[typing.List["ScalingUpPolicy"]]:
        '''
        :schema: CfnGroupPropsGroupScaling#up
        '''
        result = self._values.get("up")
        return typing.cast(typing.Optional[typing.List["ScalingUpPolicy"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupScalingMultipleMetrics",
    jsii_struct_bases=[],
    name_mapping={"expressions": "expressions", "metrics": "metrics"},
)
class CfnGroupPropsGroupScalingMultipleMetrics:
    def __init__(
        self,
        *,
        expressions: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupScalingMultipleMetricsExpressions", typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupScalingMultipleMetricsMetrics", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param expressions: 
        :param metrics: 

        :schema: CfnGroupPropsGroupScalingMultipleMetrics
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3740a569878fe77a5936cfba34ad35082ecc70d259b87ab379dfa73af32ff6fe)
            check_type(argname="argument expressions", value=expressions, expected_type=type_hints["expressions"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expressions is not None:
            self._values["expressions"] = expressions
        if metrics is not None:
            self._values["metrics"] = metrics

    @builtins.property
    def expressions(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupScalingMultipleMetricsExpressions"]]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetrics#expressions
        '''
        result = self._values.get("expressions")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupScalingMultipleMetricsExpressions"]], result)

    @builtins.property
    def metrics(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupScalingMultipleMetricsMetrics"]]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetrics#metrics
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupScalingMultipleMetricsMetrics"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupScalingMultipleMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupScalingMultipleMetricsExpressions",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression", "name": "name"},
)
class CfnGroupPropsGroupScalingMultipleMetricsExpressions:
    def __init__(
        self,
        *,
        expression: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: 
        :param name: 

        :schema: CfnGroupPropsGroupScalingMultipleMetricsExpressions
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef8c249c69d9a691c607f7980de65f28217355a31ba5467d351a4efb50024d4)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expression is not None:
            self._values["expression"] = expression
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsExpressions#expression
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsExpressions#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupScalingMultipleMetricsExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupScalingMultipleMetricsMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "dimensions": "dimensions",
        "extended_statistic": "extendedStatistic",
        "metric_name": "metricName",
        "name": "name",
        "namespace": "namespace",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class CfnGroupPropsGroupScalingMultipleMetricsMetrics:
    def __init__(
        self,
        *,
        dimensions: typing.Optional[typing.Sequence[typing.Union["Dimension", typing.Dict[builtins.str, typing.Any]]]] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        metric_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimensions: 
        :param extended_statistic: 
        :param metric_name: 
        :param name: 
        :param namespace: 
        :param statistic: 
        :param unit: 

        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaa82ccf9841e7d166c767bd3bbf234152016d8c22303f203ade70e0f3d48ac)
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument extended_statistic", value=extended_statistic, expected_type=type_hints["extended_statistic"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List["Dimension"]]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.List["Dimension"]], result)

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#extendedStatistic
        '''
        result = self._values.get("extended_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#metricName
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupScalingMultipleMetricsMetrics#unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupScalingMultipleMetricsMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupScheduling",
    jsii_struct_bases=[],
    name_mapping={"tasks": "tasks"},
)
class CfnGroupPropsGroupScheduling:
    def __init__(
        self,
        *,
        tasks: typing.Optional[typing.Sequence[typing.Union["Task", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param tasks: 

        :schema: CfnGroupPropsGroupScheduling
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33064e0dd49716025f7b3360d1ddec0a63f1d66b443a255fc6d554cf749d13a1)
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tasks is not None:
            self._values["tasks"] = tasks

    @builtins.property
    def tasks(self) -> typing.Optional[typing.List["Task"]]:
        '''
        :schema: CfnGroupPropsGroupScheduling#tasks
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.List["Task"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "availability_vs_cost": "availabilityVsCost",
        "consider_od_pricing": "considerOdPricing",
        "draining_timeout": "drainingTimeout",
        "fallback_to_od": "fallbackToOd",
        "immediate_od_recover_threshold": "immediateOdRecoverThreshold",
        "lifetime_period": "lifetimePeriod",
        "on_demand_count": "onDemandCount",
        "persistence": "persistence",
        "restrict_single_az": "restrictSingleAz",
        "revert_to_spot": "revertToSpot",
        "risk": "risk",
        "scaling_strategy": "scalingStrategy",
        "signals": "signals",
        "spin_up_time": "spinUpTime",
        "utilize_commitments": "utilizeCommitments",
        "utilize_reserved_instances": "utilizeReservedInstances",
    },
)
class CfnGroupPropsGroupStrategy:
    def __init__(
        self,
        *,
        availability_vs_cost: typing.Optional[builtins.str] = None,
        consider_od_pricing: typing.Optional[builtins.bool] = None,
        draining_timeout: typing.Optional[jsii.Number] = None,
        fallback_to_od: typing.Optional[builtins.bool] = None,
        immediate_od_recover_threshold: typing.Optional[jsii.Number] = None,
        lifetime_period: typing.Optional[builtins.str] = None,
        on_demand_count: typing.Optional[jsii.Number] = None,
        persistence: typing.Optional[typing.Union["CfnGroupPropsGroupStrategyPersistence", typing.Dict[builtins.str, typing.Any]]] = None,
        restrict_single_az: typing.Optional[builtins.bool] = None,
        revert_to_spot: typing.Optional[typing.Union["CfnGroupPropsGroupStrategyRevertToSpot", typing.Dict[builtins.str, typing.Any]]] = None,
        risk: typing.Optional[jsii.Number] = None,
        scaling_strategy: typing.Optional[typing.Union["CfnGroupPropsGroupStrategyScalingStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        signals: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupStrategySignals", typing.Dict[builtins.str, typing.Any]]]] = None,
        spin_up_time: typing.Optional[jsii.Number] = None,
        utilize_commitments: typing.Optional[builtins.bool] = None,
        utilize_reserved_instances: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param availability_vs_cost: 
        :param consider_od_pricing: 
        :param draining_timeout: 
        :param fallback_to_od: 
        :param immediate_od_recover_threshold: 
        :param lifetime_period: 
        :param on_demand_count: 
        :param persistence: 
        :param restrict_single_az: 
        :param revert_to_spot: 
        :param risk: 
        :param scaling_strategy: 
        :param signals: 
        :param spin_up_time: 
        :param utilize_commitments: 
        :param utilize_reserved_instances: 

        :schema: CfnGroupPropsGroupStrategy
        '''
        if isinstance(persistence, dict):
            persistence = CfnGroupPropsGroupStrategyPersistence(**persistence)
        if isinstance(revert_to_spot, dict):
            revert_to_spot = CfnGroupPropsGroupStrategyRevertToSpot(**revert_to_spot)
        if isinstance(scaling_strategy, dict):
            scaling_strategy = CfnGroupPropsGroupStrategyScalingStrategy(**scaling_strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2da4975b53bf256b867c857027268e918b39c0a7635f118b55815b2ee4f887)
            check_type(argname="argument availability_vs_cost", value=availability_vs_cost, expected_type=type_hints["availability_vs_cost"])
            check_type(argname="argument consider_od_pricing", value=consider_od_pricing, expected_type=type_hints["consider_od_pricing"])
            check_type(argname="argument draining_timeout", value=draining_timeout, expected_type=type_hints["draining_timeout"])
            check_type(argname="argument fallback_to_od", value=fallback_to_od, expected_type=type_hints["fallback_to_od"])
            check_type(argname="argument immediate_od_recover_threshold", value=immediate_od_recover_threshold, expected_type=type_hints["immediate_od_recover_threshold"])
            check_type(argname="argument lifetime_period", value=lifetime_period, expected_type=type_hints["lifetime_period"])
            check_type(argname="argument on_demand_count", value=on_demand_count, expected_type=type_hints["on_demand_count"])
            check_type(argname="argument persistence", value=persistence, expected_type=type_hints["persistence"])
            check_type(argname="argument restrict_single_az", value=restrict_single_az, expected_type=type_hints["restrict_single_az"])
            check_type(argname="argument revert_to_spot", value=revert_to_spot, expected_type=type_hints["revert_to_spot"])
            check_type(argname="argument risk", value=risk, expected_type=type_hints["risk"])
            check_type(argname="argument scaling_strategy", value=scaling_strategy, expected_type=type_hints["scaling_strategy"])
            check_type(argname="argument signals", value=signals, expected_type=type_hints["signals"])
            check_type(argname="argument spin_up_time", value=spin_up_time, expected_type=type_hints["spin_up_time"])
            check_type(argname="argument utilize_commitments", value=utilize_commitments, expected_type=type_hints["utilize_commitments"])
            check_type(argname="argument utilize_reserved_instances", value=utilize_reserved_instances, expected_type=type_hints["utilize_reserved_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_vs_cost is not None:
            self._values["availability_vs_cost"] = availability_vs_cost
        if consider_od_pricing is not None:
            self._values["consider_od_pricing"] = consider_od_pricing
        if draining_timeout is not None:
            self._values["draining_timeout"] = draining_timeout
        if fallback_to_od is not None:
            self._values["fallback_to_od"] = fallback_to_od
        if immediate_od_recover_threshold is not None:
            self._values["immediate_od_recover_threshold"] = immediate_od_recover_threshold
        if lifetime_period is not None:
            self._values["lifetime_period"] = lifetime_period
        if on_demand_count is not None:
            self._values["on_demand_count"] = on_demand_count
        if persistence is not None:
            self._values["persistence"] = persistence
        if restrict_single_az is not None:
            self._values["restrict_single_az"] = restrict_single_az
        if revert_to_spot is not None:
            self._values["revert_to_spot"] = revert_to_spot
        if risk is not None:
            self._values["risk"] = risk
        if scaling_strategy is not None:
            self._values["scaling_strategy"] = scaling_strategy
        if signals is not None:
            self._values["signals"] = signals
        if spin_up_time is not None:
            self._values["spin_up_time"] = spin_up_time
        if utilize_commitments is not None:
            self._values["utilize_commitments"] = utilize_commitments
        if utilize_reserved_instances is not None:
            self._values["utilize_reserved_instances"] = utilize_reserved_instances

    @builtins.property
    def availability_vs_cost(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupStrategy#availabilityVsCost
        '''
        result = self._values.get("availability_vs_cost")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consider_od_pricing(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategy#considerODPricing
        '''
        result = self._values.get("consider_od_pricing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def draining_timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupStrategy#drainingTimeout
        '''
        result = self._values.get("draining_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fallback_to_od(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategy#fallbackToOd
        '''
        result = self._values.get("fallback_to_od")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def immediate_od_recover_threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupStrategy#immediateODRecoverThreshold
        '''
        result = self._values.get("immediate_od_recover_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lifetime_period(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupStrategy#lifetimePeriod
        '''
        result = self._values.get("lifetime_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_count(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupStrategy#onDemandCount
        '''
        result = self._values.get("on_demand_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def persistence(self) -> typing.Optional["CfnGroupPropsGroupStrategyPersistence"]:
        '''
        :schema: CfnGroupPropsGroupStrategy#persistence
        '''
        result = self._values.get("persistence")
        return typing.cast(typing.Optional["CfnGroupPropsGroupStrategyPersistence"], result)

    @builtins.property
    def restrict_single_az(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategy#restrictSingleAz
        '''
        result = self._values.get("restrict_single_az")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def revert_to_spot(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupStrategyRevertToSpot"]:
        '''
        :schema: CfnGroupPropsGroupStrategy#revertToSpot
        '''
        result = self._values.get("revert_to_spot")
        return typing.cast(typing.Optional["CfnGroupPropsGroupStrategyRevertToSpot"], result)

    @builtins.property
    def risk(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupStrategy#risk
        '''
        result = self._values.get("risk")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scaling_strategy(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupStrategyScalingStrategy"]:
        '''
        :schema: CfnGroupPropsGroupStrategy#scalingStrategy
        '''
        result = self._values.get("scaling_strategy")
        return typing.cast(typing.Optional["CfnGroupPropsGroupStrategyScalingStrategy"], result)

    @builtins.property
    def signals(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupStrategySignals"]]:
        '''
        :schema: CfnGroupPropsGroupStrategy#signals
        '''
        result = self._values.get("signals")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupStrategySignals"]], result)

    @builtins.property
    def spin_up_time(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupStrategy#spinUpTime
        '''
        result = self._values.get("spin_up_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def utilize_commitments(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategy#utilizeCommitments
        '''
        result = self._values.get("utilize_commitments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def utilize_reserved_instances(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategy#utilizeReservedInstances
        '''
        result = self._values.get("utilize_reserved_instances")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupStrategyPersistence",
    jsii_struct_bases=[],
    name_mapping={
        "block_devices_mode": "blockDevicesMode",
        "should_persist_block_devices": "shouldPersistBlockDevices",
        "should_persist_private_ip": "shouldPersistPrivateIp",
        "should_persist_root_device": "shouldPersistRootDevice",
    },
)
class CfnGroupPropsGroupStrategyPersistence:
    def __init__(
        self,
        *,
        block_devices_mode: typing.Optional[builtins.str] = None,
        should_persist_block_devices: typing.Optional[builtins.bool] = None,
        should_persist_private_ip: typing.Optional[builtins.bool] = None,
        should_persist_root_device: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param block_devices_mode: 
        :param should_persist_block_devices: 
        :param should_persist_private_ip: 
        :param should_persist_root_device: 

        :schema: CfnGroupPropsGroupStrategyPersistence
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b297029ffe121286b26d9465f36540fafd3ec99a3844b506301b58e1ff49487)
            check_type(argname="argument block_devices_mode", value=block_devices_mode, expected_type=type_hints["block_devices_mode"])
            check_type(argname="argument should_persist_block_devices", value=should_persist_block_devices, expected_type=type_hints["should_persist_block_devices"])
            check_type(argname="argument should_persist_private_ip", value=should_persist_private_ip, expected_type=type_hints["should_persist_private_ip"])
            check_type(argname="argument should_persist_root_device", value=should_persist_root_device, expected_type=type_hints["should_persist_root_device"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if block_devices_mode is not None:
            self._values["block_devices_mode"] = block_devices_mode
        if should_persist_block_devices is not None:
            self._values["should_persist_block_devices"] = should_persist_block_devices
        if should_persist_private_ip is not None:
            self._values["should_persist_private_ip"] = should_persist_private_ip
        if should_persist_root_device is not None:
            self._values["should_persist_root_device"] = should_persist_root_device

    @builtins.property
    def block_devices_mode(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupStrategyPersistence#blockDevicesMode
        '''
        result = self._values.get("block_devices_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def should_persist_block_devices(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategyPersistence#shouldPersistBlockDevices
        '''
        result = self._values.get("should_persist_block_devices")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def should_persist_private_ip(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategyPersistence#shouldPersistPrivateIp
        '''
        result = self._values.get("should_persist_private_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def should_persist_root_device(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategyPersistence#shouldPersistRootDevice
        '''
        result = self._values.get("should_persist_root_device")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupStrategyPersistence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupStrategyRevertToSpot",
    jsii_struct_bases=[],
    name_mapping={"perform_at": "performAt", "time_windows": "timeWindows"},
)
class CfnGroupPropsGroupStrategyRevertToSpot:
    def __init__(
        self,
        *,
        perform_at: typing.Optional[builtins.str] = None,
        time_windows: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param perform_at: 
        :param time_windows: 

        :schema: CfnGroupPropsGroupStrategyRevertToSpot
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4038443c669504fd62a7fe192dbd44e2b8f11183a61aeabb8503bd9d99393812)
            check_type(argname="argument perform_at", value=perform_at, expected_type=type_hints["perform_at"])
            check_type(argname="argument time_windows", value=time_windows, expected_type=type_hints["time_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if perform_at is not None:
            self._values["perform_at"] = perform_at
        if time_windows is not None:
            self._values["time_windows"] = time_windows

    @builtins.property
    def perform_at(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupStrategyRevertToSpot#performAt
        '''
        result = self._values.get("perform_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_windows(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupStrategyRevertToSpot#timeWindows
        '''
        result = self._values.get("time_windows")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupStrategyRevertToSpot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupStrategyScalingStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "terminate_at_end_of_billing_hour": "terminateAtEndOfBillingHour",
        "termination_policy": "terminationPolicy",
    },
)
class CfnGroupPropsGroupStrategyScalingStrategy:
    def __init__(
        self,
        *,
        terminate_at_end_of_billing_hour: typing.Optional[builtins.bool] = None,
        termination_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param terminate_at_end_of_billing_hour: 
        :param termination_policy: 

        :schema: CfnGroupPropsGroupStrategyScalingStrategy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c4ea38972417a6e950105298c25794fd879cf0cab3a44304bbd342cb72329b)
            check_type(argname="argument terminate_at_end_of_billing_hour", value=terminate_at_end_of_billing_hour, expected_type=type_hints["terminate_at_end_of_billing_hour"])
            check_type(argname="argument termination_policy", value=termination_policy, expected_type=type_hints["termination_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if terminate_at_end_of_billing_hour is not None:
            self._values["terminate_at_end_of_billing_hour"] = terminate_at_end_of_billing_hour
        if termination_policy is not None:
            self._values["termination_policy"] = termination_policy

    @builtins.property
    def terminate_at_end_of_billing_hour(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupStrategyScalingStrategy#terminateAtEndOfBillingHour
        '''
        result = self._values.get("terminate_at_end_of_billing_hour")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def termination_policy(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupStrategyScalingStrategy#terminationPolicy
        '''
        result = self._values.get("termination_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupStrategyScalingStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupStrategySignals",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "timeout": "timeout"},
)
class CfnGroupPropsGroupStrategySignals:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: 
        :param timeout: 

        :schema: CfnGroupPropsGroupStrategySignals
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6fa076e7565d225c699363134fe3687bb029836ecfe7edf06e241246bd4dfc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupStrategySignals#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupStrategySignals#timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupStrategySignals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegration",
    jsii_struct_bases=[],
    name_mapping={
        "chef": "chef",
        "code_deploy": "codeDeploy",
        "datadog": "datadog",
        "docker_swarm": "dockerSwarm",
        "ecs": "ecs",
        "elastic_beanstalk": "elasticBeanstalk",
        "gitlab": "gitlab",
        "jenkins": "jenkins",
        "kubernetes": "kubernetes",
        "mesosphere": "mesosphere",
        "mlb_runtime": "mlbRuntime",
        "nomad": "nomad",
        "ops_works": "opsWorks",
        "rancher": "rancher",
        "right_scale": "rightScale",
        "route53": "route53",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegration:
    def __init__(
        self,
        *,
        chef: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationChef", typing.Dict[builtins.str, typing.Any]]] = None,
        code_deploy: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_swarm: typing.Optional[typing.Union["DockerSwarm", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs: typing.Optional[typing.Union["Ecs", typing.Dict[builtins.str, typing.Any]]] = None,
        elastic_beanstalk: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationGitlab", typing.Dict[builtins.str, typing.Any]]] = None,
        jenkins: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationJenkins", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["Kubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        mesosphere: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationMesosphere", typing.Dict[builtins.str, typing.Any]]] = None,
        mlb_runtime: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime", typing.Dict[builtins.str, typing.Any]]] = None,
        nomad: typing.Optional[typing.Union["Nomad", typing.Dict[builtins.str, typing.Any]]] = None,
        ops_works: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks", typing.Dict[builtins.str, typing.Any]]] = None,
        rancher: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationRancher", typing.Dict[builtins.str, typing.Any]]] = None,
        right_scale: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationRightScale", typing.Dict[builtins.str, typing.Any]]] = None,
        route53: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationRoute53", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param chef: 
        :param code_deploy: 
        :param datadog: 
        :param docker_swarm: 
        :param ecs: 
        :param elastic_beanstalk: 
        :param gitlab: 
        :param jenkins: 
        :param kubernetes: 
        :param mesosphere: 
        :param mlb_runtime: 
        :param nomad: 
        :param ops_works: 
        :param rancher: 
        :param right_scale: 
        :param route53: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegration
        '''
        if isinstance(chef, dict):
            chef = CfnGroupPropsGroupThirdPartiesIntegrationChef(**chef)
        if isinstance(code_deploy, dict):
            code_deploy = CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy(**code_deploy)
        if isinstance(datadog, dict):
            datadog = CfnGroupPropsGroupThirdPartiesIntegrationDatadog(**datadog)
        if isinstance(docker_swarm, dict):
            docker_swarm = DockerSwarm(**docker_swarm)
        if isinstance(ecs, dict):
            ecs = Ecs(**ecs)
        if isinstance(elastic_beanstalk, dict):
            elastic_beanstalk = CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk(**elastic_beanstalk)
        if isinstance(gitlab, dict):
            gitlab = CfnGroupPropsGroupThirdPartiesIntegrationGitlab(**gitlab)
        if isinstance(jenkins, dict):
            jenkins = CfnGroupPropsGroupThirdPartiesIntegrationJenkins(**jenkins)
        if isinstance(kubernetes, dict):
            kubernetes = Kubernetes(**kubernetes)
        if isinstance(mesosphere, dict):
            mesosphere = CfnGroupPropsGroupThirdPartiesIntegrationMesosphere(**mesosphere)
        if isinstance(mlb_runtime, dict):
            mlb_runtime = CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime(**mlb_runtime)
        if isinstance(nomad, dict):
            nomad = Nomad(**nomad)
        if isinstance(ops_works, dict):
            ops_works = CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks(**ops_works)
        if isinstance(rancher, dict):
            rancher = CfnGroupPropsGroupThirdPartiesIntegrationRancher(**rancher)
        if isinstance(right_scale, dict):
            right_scale = CfnGroupPropsGroupThirdPartiesIntegrationRightScale(**right_scale)
        if isinstance(route53, dict):
            route53 = CfnGroupPropsGroupThirdPartiesIntegrationRoute53(**route53)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5555d4f9d204203ac07f07c71c7c81553d8076fdf497aa0a812e17238a23a8)
            check_type(argname="argument chef", value=chef, expected_type=type_hints["chef"])
            check_type(argname="argument code_deploy", value=code_deploy, expected_type=type_hints["code_deploy"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument docker_swarm", value=docker_swarm, expected_type=type_hints["docker_swarm"])
            check_type(argname="argument ecs", value=ecs, expected_type=type_hints["ecs"])
            check_type(argname="argument elastic_beanstalk", value=elastic_beanstalk, expected_type=type_hints["elastic_beanstalk"])
            check_type(argname="argument gitlab", value=gitlab, expected_type=type_hints["gitlab"])
            check_type(argname="argument jenkins", value=jenkins, expected_type=type_hints["jenkins"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument mesosphere", value=mesosphere, expected_type=type_hints["mesosphere"])
            check_type(argname="argument mlb_runtime", value=mlb_runtime, expected_type=type_hints["mlb_runtime"])
            check_type(argname="argument nomad", value=nomad, expected_type=type_hints["nomad"])
            check_type(argname="argument ops_works", value=ops_works, expected_type=type_hints["ops_works"])
            check_type(argname="argument rancher", value=rancher, expected_type=type_hints["rancher"])
            check_type(argname="argument right_scale", value=right_scale, expected_type=type_hints["right_scale"])
            check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chef is not None:
            self._values["chef"] = chef
        if code_deploy is not None:
            self._values["code_deploy"] = code_deploy
        if datadog is not None:
            self._values["datadog"] = datadog
        if docker_swarm is not None:
            self._values["docker_swarm"] = docker_swarm
        if ecs is not None:
            self._values["ecs"] = ecs
        if elastic_beanstalk is not None:
            self._values["elastic_beanstalk"] = elastic_beanstalk
        if gitlab is not None:
            self._values["gitlab"] = gitlab
        if jenkins is not None:
            self._values["jenkins"] = jenkins
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if mesosphere is not None:
            self._values["mesosphere"] = mesosphere
        if mlb_runtime is not None:
            self._values["mlb_runtime"] = mlb_runtime
        if nomad is not None:
            self._values["nomad"] = nomad
        if ops_works is not None:
            self._values["ops_works"] = ops_works
        if rancher is not None:
            self._values["rancher"] = rancher
        if right_scale is not None:
            self._values["right_scale"] = right_scale
        if route53 is not None:
            self._values["route53"] = route53

    @builtins.property
    def chef(self) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationChef"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#chef
        '''
        result = self._values.get("chef")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationChef"], result)

    @builtins.property
    def code_deploy(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#codeDeploy
        '''
        result = self._values.get("code_deploy")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationDatadog"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#datadog
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationDatadog"], result)

    @builtins.property
    def docker_swarm(self) -> typing.Optional["DockerSwarm"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#dockerSwarm
        '''
        result = self._values.get("docker_swarm")
        return typing.cast(typing.Optional["DockerSwarm"], result)

    @builtins.property
    def ecs(self) -> typing.Optional["Ecs"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#ecs
        '''
        result = self._values.get("ecs")
        return typing.cast(typing.Optional["Ecs"], result)

    @builtins.property
    def elastic_beanstalk(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#elasticBeanstalk
        '''
        result = self._values.get("elastic_beanstalk")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk"], result)

    @builtins.property
    def gitlab(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationGitlab"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#gitlab
        '''
        result = self._values.get("gitlab")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationGitlab"], result)

    @builtins.property
    def jenkins(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkins"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#jenkins
        '''
        result = self._values.get("jenkins")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkins"], result)

    @builtins.property
    def kubernetes(self) -> typing.Optional["Kubernetes"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#kubernetes
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["Kubernetes"], result)

    @builtins.property
    def mesosphere(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationMesosphere"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#mesosphere
        '''
        result = self._values.get("mesosphere")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationMesosphere"], result)

    @builtins.property
    def mlb_runtime(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#mlbRuntime
        '''
        result = self._values.get("mlb_runtime")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime"], result)

    @builtins.property
    def nomad(self) -> typing.Optional["Nomad"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#nomad
        '''
        result = self._values.get("nomad")
        return typing.cast(typing.Optional["Nomad"], result)

    @builtins.property
    def ops_works(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#opsWorks
        '''
        result = self._values.get("ops_works")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks"], result)

    @builtins.property
    def rancher(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationRancher"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#rancher
        '''
        result = self._values.get("rancher")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationRancher"], result)

    @builtins.property
    def right_scale(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationRightScale"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#rightScale
        '''
        result = self._values.get("right_scale")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationRightScale"], result)

    @builtins.property
    def route53(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationRoute53"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegration#route53
        '''
        result = self._values.get("route53")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationRoute53"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationChef",
    jsii_struct_bases=[],
    name_mapping={
        "chef_server": "chefServer",
        "chef_version": "chefVersion",
        "organization": "organization",
        "pem_key": "pemKey",
        "user": "user",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationChef:
    def __init__(
        self,
        *,
        chef_server: typing.Optional[builtins.str] = None,
        chef_version: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        pem_key: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param chef_server: 
        :param chef_version: 
        :param organization: 
        :param pem_key: 
        :param user: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationChef
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8ab428ecf44992772678cee610d0647301230bc713d19ada85eb16bf1b283d)
            check_type(argname="argument chef_server", value=chef_server, expected_type=type_hints["chef_server"])
            check_type(argname="argument chef_version", value=chef_version, expected_type=type_hints["chef_version"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument pem_key", value=pem_key, expected_type=type_hints["pem_key"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chef_server is not None:
            self._values["chef_server"] = chef_server
        if chef_version is not None:
            self._values["chef_version"] = chef_version
        if organization is not None:
            self._values["organization"] = organization
        if pem_key is not None:
            self._values["pem_key"] = pem_key
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def chef_server(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationChef#chefServer
        '''
        result = self._values.get("chef_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chef_version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationChef#chefVersion
        '''
        result = self._values.get("chef_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationChef#organization
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationChef#pemKey
        '''
        result = self._values.get("pem_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationChef#user
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationChef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy",
    jsii_struct_bases=[],
    name_mapping={
        "clean_up_on_failure": "cleanUpOnFailure",
        "deployment_groups": "deploymentGroups",
        "terminate_instance_on_failure": "terminateInstanceOnFailure",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy:
    def __init__(
        self,
        *,
        clean_up_on_failure: typing.Optional[builtins.bool] = None,
        deployment_groups: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups", typing.Dict[builtins.str, typing.Any]]]] = None,
        terminate_instance_on_failure: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param clean_up_on_failure: 
        :param deployment_groups: 
        :param terminate_instance_on_failure: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd7671b9bec15a81fe403e32e96b93775bc11f0ef34ed74ddc45c7d34bfb247)
            check_type(argname="argument clean_up_on_failure", value=clean_up_on_failure, expected_type=type_hints["clean_up_on_failure"])
            check_type(argname="argument deployment_groups", value=deployment_groups, expected_type=type_hints["deployment_groups"])
            check_type(argname="argument terminate_instance_on_failure", value=terminate_instance_on_failure, expected_type=type_hints["terminate_instance_on_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if clean_up_on_failure is not None:
            self._values["clean_up_on_failure"] = clean_up_on_failure
        if deployment_groups is not None:
            self._values["deployment_groups"] = deployment_groups
        if terminate_instance_on_failure is not None:
            self._values["terminate_instance_on_failure"] = terminate_instance_on_failure

    @builtins.property
    def clean_up_on_failure(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy#cleanUpOnFailure
        '''
        result = self._values.get("clean_up_on_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deployment_groups(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups"]]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy#deploymentGroups
        '''
        result = self._values.get("deployment_groups")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups"]], result)

    @builtins.property
    def terminate_instance_on_failure(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy#terminateInstanceOnFailure
        '''
        result = self._values.get("terminate_instance_on_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "deployment_group_name": "deploymentGroupName",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_name: 
        :param deployment_group_name: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332a3aceba069d7e5c5c597c6e06d2938fbf30f33f38e6949539f8cbc776be68)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups#applicationName
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups#deploymentGroupName
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationDatadog",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "metrics_to_report": "metricsToReport"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationDatadog:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        metrics_to_report: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: 
        :param metrics_to_report: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationDatadog
        '''
        if isinstance(metrics_to_report, dict):
            metrics_to_report = CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport(**metrics_to_report)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d131c237712829165735ac4ee4ed29626b1fa1ce7b039982556375fca808cd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metrics_to_report", value=metrics_to_report, expected_type=type_hints["metrics_to_report"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if metrics_to_report is not None:
            self._values["metrics_to_report"] = metrics_to_report

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationDatadog#id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics_to_report(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationDatadog#metricsToReport
        '''
        result = self._values.get("metrics_to_report")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport",
    jsii_struct_bases=[],
    name_mapping={"metrics_list": "metricsList", "tags": "tags"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport:
    def __init__(
        self,
        *,
        metrics_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param metrics_list: 
        :param tags: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81102ecd411438dc28cfa28d178d5e8ec04731a39c218af6f947b73523d711e)
            check_type(argname="argument metrics_list", value=metrics_list, expected_type=type_hints["metrics_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_list is not None:
            self._values["metrics_list"] = metrics_list
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def metrics_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport#metricsList
        '''
        result = self._values.get("metrics_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport#tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_preferences": "deploymentPreferences",
        "environment_id": "environmentId",
        "managed_actions": "managedActions",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk:
    def __init__(
        self,
        *,
        deployment_preferences: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_id: typing.Optional[builtins.str] = None,
        managed_actions: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deployment_preferences: 
        :param environment_id: 
        :param managed_actions: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk
        '''
        if isinstance(deployment_preferences, dict):
            deployment_preferences = CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences(**deployment_preferences)
        if isinstance(managed_actions, dict):
            managed_actions = CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions(**managed_actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ab9b6815b14d0047e40577bff74c2428d454b73f6903a2e7db435e0b4e434d)
            check_type(argname="argument deployment_preferences", value=deployment_preferences, expected_type=type_hints["deployment_preferences"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            check_type(argname="argument managed_actions", value=managed_actions, expected_type=type_hints["managed_actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_preferences is not None:
            self._values["deployment_preferences"] = deployment_preferences
        if environment_id is not None:
            self._values["environment_id"] = environment_id
        if managed_actions is not None:
            self._values["managed_actions"] = managed_actions

    @builtins.property
    def deployment_preferences(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk#deploymentPreferences
        '''
        result = self._values.get("deployment_preferences")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences"], result)

    @builtins.property
    def environment_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk#environmentId
        '''
        result = self._values.get("environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_actions(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk#managedActions
        '''
        result = self._values.get("managed_actions")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_roll": "automaticRoll",
        "batch_size_percentage": "batchSizePercentage",
        "grace_period": "gracePeriod",
        "strategy": "strategy",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences:
    def __init__(
        self,
        *,
        automatic_roll: typing.Optional[builtins.bool] = None,
        batch_size_percentage: typing.Optional[jsii.Number] = None,
        grace_period: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[typing.Union[BeanStalkStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automatic_roll: 
        :param batch_size_percentage: 
        :param grace_period: 
        :param strategy: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences
        '''
        if isinstance(strategy, dict):
            strategy = BeanStalkStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9853dcdedddfcb098eb174885dd0adcc3ccbd7f17b16408ca9414b10a0f73a5)
            check_type(argname="argument automatic_roll", value=automatic_roll, expected_type=type_hints["automatic_roll"])
            check_type(argname="argument batch_size_percentage", value=batch_size_percentage, expected_type=type_hints["batch_size_percentage"])
            check_type(argname="argument grace_period", value=grace_period, expected_type=type_hints["grace_period"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_roll is not None:
            self._values["automatic_roll"] = automatic_roll
        if batch_size_percentage is not None:
            self._values["batch_size_percentage"] = batch_size_percentage
        if grace_period is not None:
            self._values["grace_period"] = grace_period
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def automatic_roll(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences#automaticRoll
        '''
        result = self._values.get("automatic_roll")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def batch_size_percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences#batchSizePercentage
        '''
        result = self._values.get("batch_size_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grace_period(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences#gracePeriod
        '''
        result = self._values.get("grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strategy(self) -> typing.Optional[BeanStalkStrategy]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences#strategy
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[BeanStalkStrategy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions",
    jsii_struct_bases=[],
    name_mapping={"platform_update": "platformUpdate"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions:
    def __init__(
        self,
        *,
        platform_update: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param platform_update: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions
        '''
        if isinstance(platform_update, dict):
            platform_update = CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate(**platform_update)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec5285bd3f6d02d365044c8106f9da7c0b0513810adf92179f602697429d50c)
            check_type(argname="argument platform_update", value=platform_update, expected_type=type_hints["platform_update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if platform_update is not None:
            self._values["platform_update"] = platform_update

    @builtins.property
    def platform_update(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions#platformUpdate
        '''
        result = self._values.get("platform_update")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate",
    jsii_struct_bases=[],
    name_mapping={
        "instance_refresh_enabled": "instanceRefreshEnabled",
        "perform_at": "performAt",
        "time_window": "timeWindow",
        "update_level": "updateLevel",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate:
    def __init__(
        self,
        *,
        instance_refresh_enabled: typing.Optional[builtins.bool] = None,
        perform_at: typing.Optional[builtins.str] = None,
        time_window: typing.Optional[builtins.str] = None,
        update_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_refresh_enabled: 
        :param perform_at: 
        :param time_window: 
        :param update_level: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34c3a0df419b8708f1c6a95da6774af5e4b10e22ef10fbbe04430361e619828)
            check_type(argname="argument instance_refresh_enabled", value=instance_refresh_enabled, expected_type=type_hints["instance_refresh_enabled"])
            check_type(argname="argument perform_at", value=perform_at, expected_type=type_hints["perform_at"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
            check_type(argname="argument update_level", value=update_level, expected_type=type_hints["update_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_refresh_enabled is not None:
            self._values["instance_refresh_enabled"] = instance_refresh_enabled
        if perform_at is not None:
            self._values["perform_at"] = perform_at
        if time_window is not None:
            self._values["time_window"] = time_window
        if update_level is not None:
            self._values["update_level"] = update_level

    @builtins.property
    def instance_refresh_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate#instanceRefreshEnabled
        '''
        result = self._values.get("instance_refresh_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def perform_at(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate#performAt
        '''
        result = self._values.get("perform_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_window(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate#timeWindow
        '''
        result = self._values.get("time_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_level(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate#updateLevel
        '''
        result = self._values.get("update_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationGitlab",
    jsii_struct_bases=[],
    name_mapping={"runner": "runner"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationGitlab:
    def __init__(
        self,
        *,
        runner: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param runner: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationGitlab
        '''
        if isinstance(runner, dict):
            runner = CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner(**runner)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfee26a2ab04a4b287dc6b512a93fcec187f22a51a54979560b0757189b633a)
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if runner is not None:
            self._values["runner"] = runner

    @builtins.property
    def runner(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationGitlab#runner
        '''
        result = self._values.get("runner")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationGitlab(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner",
    jsii_struct_bases=[],
    name_mapping={"is_enabled": "isEnabled"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner:
    def __init__(self, *, is_enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param is_enabled: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec04634d1252a709db9e252467b2f36438ffcf23e3ce6db6966e680f763368b6)
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationJenkins",
    jsii_struct_bases=[],
    name_mapping={"connection_method": "connectionMethod"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationJenkins:
    def __init__(
        self,
        *,
        connection_method: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection_method: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkins
        '''
        if isinstance(connection_method, dict):
            connection_method = CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod(**connection_method)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3eec9f2efab166b23d53e0fcb0a2048ebb58877a12f770ce9ff0c8005cec3d)
            check_type(argname="argument connection_method", value=connection_method, expected_type=type_hints["connection_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_method is not None:
            self._values["connection_method"] = connection_method

    @builtins.property
    def connection_method(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkins#connectionMethod
        '''
        result = self._values.get("connection_method")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationJenkins(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod",
    jsii_struct_bases=[],
    name_mapping={
        "jnlp": "jnlp",
        "manually_connection": "manuallyConnection",
        "ssh": "ssh",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod:
    def __init__(
        self,
        *,
        jnlp: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp", typing.Dict[builtins.str, typing.Any]]] = None,
        manually_connection: typing.Optional[builtins.bool] = None,
        ssh: typing.Optional[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param jnlp: 
        :param manually_connection: 
        :param ssh: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod
        '''
        if isinstance(jnlp, dict):
            jnlp = CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp(**jnlp)
        if isinstance(ssh, dict):
            ssh = CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh(**ssh)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b322341fefccaa1dbeb4f7bf234cf26b12698142426ff1dca4acaa9e9d378a8)
            check_type(argname="argument jnlp", value=jnlp, expected_type=type_hints["jnlp"])
            check_type(argname="argument manually_connection", value=manually_connection, expected_type=type_hints["manually_connection"])
            check_type(argname="argument ssh", value=ssh, expected_type=type_hints["ssh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jnlp is not None:
            self._values["jnlp"] = jnlp
        if manually_connection is not None:
            self._values["manually_connection"] = manually_connection
        if ssh is not None:
            self._values["ssh"] = ssh

    @builtins.property
    def jnlp(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod#jnlp
        '''
        result = self._values.get("jnlp")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp"], result)

    @builtins.property
    def manually_connection(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod#manuallyConnection
        '''
        result = self._values.get("manually_connection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh(
        self,
    ) -> typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh"]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod#ssh
        '''
        result = self._values.get("ssh")
        return typing.cast(typing.Optional["CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp",
    jsii_struct_bases=[],
    name_mapping={
        "master_ip": "masterIp",
        "master_port": "masterPort",
        "password": "password",
        "token": "token",
        "user_name": "userName",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp:
    def __init__(
        self,
        *,
        master_ip: typing.Optional[builtins.str] = None,
        master_port: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param master_ip: 
        :param master_port: 
        :param password: 
        :param token: 
        :param user_name: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2083d3376cfd70d24c4d470e08c26370cf05fa9624999d265863af3986359be7)
            check_type(argname="argument master_ip", value=master_ip, expected_type=type_hints["master_ip"])
            check_type(argname="argument master_port", value=master_port, expected_type=type_hints["master_port"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if master_ip is not None:
            self._values["master_ip"] = master_ip
        if master_port is not None:
            self._values["master_port"] = master_port
        if password is not None:
            self._values["password"] = password
        if token is not None:
            self._values["token"] = token
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def master_ip(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp#masterIP
        '''
        result = self._values.get("master_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_port(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp#masterPort
        '''
        result = self._values.get("master_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp#password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp#token
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp#userName
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh",
    jsii_struct_bases=[],
    name_mapping={"ssh_public_key": "sshPublicKey"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh:
    def __init__(self, *, ssh_public_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param ssh_public_key: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea48e69031699e0e4e8a84781cbaab80d140f3f9ff9d08124634ba65b8a1016)
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ssh_public_key is not None:
            self._values["ssh_public_key"] = ssh_public_key

    @builtins.property
    def ssh_public_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh#sshPublicKey
        '''
        result = self._values.get("ssh_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationMesosphere",
    jsii_struct_bases=[],
    name_mapping={"api_server": "apiServer"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationMesosphere:
    def __init__(self, *, api_server: typing.Optional[builtins.str] = None) -> None:
        '''
        :param api_server: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationMesosphere
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4db328a799f95f0060615a6510b435a68af1b6753c104945aca17944574f343)
            check_type(argname="argument api_server", value=api_server, expected_type=type_hints["api_server"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_server is not None:
            self._values["api_server"] = api_server

    @builtins.property
    def api_server(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationMesosphere#apiServer
        '''
        result = self._values.get("api_server")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationMesosphere(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime",
    jsii_struct_bases=[],
    name_mapping={"deployment_id": "deploymentId"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime:
    def __init__(self, *, deployment_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param deployment_id: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46be76a5581f65142ef80b58da02fa335a158862d3e6d4c7ba7106bc8d9b89a)
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_id is not None:
            self._values["deployment_id"] = deployment_id

    @builtins.property
    def deployment_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime#deploymentId
        '''
        result = self._values.get("deployment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks",
    jsii_struct_bases=[],
    name_mapping={"layer_id": "layerId", "stack_type": "stackType"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks:
    def __init__(
        self,
        *,
        layer_id: typing.Optional[builtins.str] = None,
        stack_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param layer_id: 
        :param stack_type: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12778848891ca597f38262063a51c782da69e0d4deb0845f19c821d0e1add0e)
            check_type(argname="argument layer_id", value=layer_id, expected_type=type_hints["layer_id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if layer_id is not None:
            self._values["layer_id"] = layer_id
        if stack_type is not None:
            self._values["stack_type"] = stack_type

    @builtins.property
    def layer_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks#layerId
        '''
        result = self._values.get("layer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks#stackType
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationRancher",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "master_host": "masterHost",
        "secret_key": "secretKey",
        "version": "version",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationRancher:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        master_host: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: 
        :param master_host: 
        :param secret_key: 
        :param version: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRancher
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe57865056b712b1203733a620af0c22146831c27c3c778b096af044c1d0ecf)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument master_host", value=master_host, expected_type=type_hints["master_host"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if master_host is not None:
            self._values["master_host"] = master_host
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRancher#accessKey
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_host(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRancher#masterHost
        '''
        result = self._values.get("master_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRancher#secretKey
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRancher#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationRancher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationRightScale",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "refresh_token": "refreshToken",
        "region": "region",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationRightScale:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        refresh_token: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: 
        :param refresh_token: 
        :param region: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRightScale
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7611add7b872b59867fac77c98f26b9d1cacc6398b8c5554ee470334f28acd)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRightScale#accountId
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRightScale#refreshToken
        '''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRightScale#region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationRightScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationRoute53",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationRoute53:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param domains: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91e02e5dec3c5e28d39ef2f85de9f0d848d41aafa47995b9518218e4ac29311)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domains is not None:
            self._values["domains"] = domains

    @builtins.property
    def domains(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains"]]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53#domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationRoute53(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone_id": "hostedZoneId",
        "record_sets": "recordSets",
        "record_set_type": "recordSetType",
        "spotinst_account_id": "spotinstAccountId",
    },
)
class CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains:
    def __init__(
        self,
        *,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        record_sets: typing.Optional[typing.Sequence[typing.Union["CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets", typing.Dict[builtins.str, typing.Any]]]] = None,
        record_set_type: typing.Optional[builtins.str] = None,
        spotinst_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hosted_zone_id: 
        :param record_sets: 
        :param record_set_type: 
        :param spotinst_account_id: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8c1d153188d5f73fb2870c92acbd09c410dea5e6d93d195cbd36c80f468e25)
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            check_type(argname="argument record_sets", value=record_sets, expected_type=type_hints["record_sets"])
            check_type(argname="argument record_set_type", value=record_set_type, expected_type=type_hints["record_set_type"])
            check_type(argname="argument spotinst_account_id", value=spotinst_account_id, expected_type=type_hints["spotinst_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id
        if record_sets is not None:
            self._values["record_sets"] = record_sets
        if record_set_type is not None:
            self._values["record_set_type"] = record_set_type
        if spotinst_account_id is not None:
            self._values["spotinst_account_id"] = spotinst_account_id

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains#hostedZoneId
        '''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_sets(
        self,
    ) -> typing.Optional[typing.List["CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets"]]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains#recordSets
        '''
        result = self._values.get("record_sets")
        return typing.cast(typing.Optional[typing.List["CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets"]], result)

    @builtins.property
    def record_set_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains#recordSetType
        '''
        result = self._values.get("record_set_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spotinst_account_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains#spotinstAccountId
        '''
        result = self._values.get("spotinst_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "use_public_dns": "usePublicDns"},
)
class CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        use_public_dns: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: 
        :param use_public_dns: 

        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a47d3270e9dea2522bb94845522a92c7b7215d7c7c71978e76162d3f2e87979)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument use_public_dns", value=use_public_dns, expected_type=type_hints["use_public_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if use_public_dns is not None:
            self._values["use_public_dns"] = use_public_dns

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_public_dns(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets#usePublicDns
        '''
        result = self._values.get("use_public_dns")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Dimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Dimension:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param value: 

        :schema: Dimension
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b163980c9edf9068b97ebe8273844308a50a56a73f7eb96604b080ddac8537)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Dimension#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Dimension#value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Dimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.DockerSwarm",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scale": "autoScale",
        "master_host": "masterHost",
        "master_port": "masterPort",
        "tls_config": "tlsConfig",
    },
)
class DockerSwarm:
    def __init__(
        self,
        *,
        auto_scale: typing.Optional[typing.Union["DockerSwarmAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        master_host: typing.Optional[builtins.str] = None,
        master_port: typing.Optional[jsii.Number] = None,
        tls_config: typing.Optional[typing.Union["TlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_scale: 
        :param master_host: 
        :param master_port: 
        :param tls_config: 

        :schema: DockerSwarm
        '''
        if isinstance(auto_scale, dict):
            auto_scale = DockerSwarmAutoScale(**auto_scale)
        if isinstance(tls_config, dict):
            tls_config = TlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87debdc2b90d72dd4d8a6277c3f23483225db7b3ea2d5f2c5d29a707ab27192)
            check_type(argname="argument auto_scale", value=auto_scale, expected_type=type_hints["auto_scale"])
            check_type(argname="argument master_host", value=master_host, expected_type=type_hints["master_host"])
            check_type(argname="argument master_port", value=master_port, expected_type=type_hints["master_port"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scale is not None:
            self._values["auto_scale"] = auto_scale
        if master_host is not None:
            self._values["master_host"] = master_host
        if master_port is not None:
            self._values["master_port"] = master_port
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def auto_scale(self) -> typing.Optional["DockerSwarmAutoScale"]:
        '''
        :schema: DockerSwarm#autoScale
        '''
        result = self._values.get("auto_scale")
        return typing.cast(typing.Optional["DockerSwarmAutoScale"], result)

    @builtins.property
    def master_host(self) -> typing.Optional[builtins.str]:
        '''
        :schema: DockerSwarm#masterHost
        '''
        result = self._values.get("master_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_port(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: DockerSwarm#masterPort
        '''
        result = self._values.get("master_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_config(self) -> typing.Optional["TlsConfig"]:
        '''
        :schema: DockerSwarm#tlsConfig
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["TlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerSwarm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.DockerSwarmAutoScale",
    jsii_struct_bases=[],
    name_mapping={
        "cooldown": "cooldown",
        "down": "down",
        "headroom": "headroom",
        "is_enabled": "isEnabled",
        "labels": "labels",
    },
)
class DockerSwarmAutoScale:
    def __init__(
        self,
        *,
        cooldown: typing.Optional[jsii.Number] = None,
        down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
        headroom: typing.Optional[typing.Union["Headroom", typing.Dict[builtins.str, typing.Any]]] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param cooldown: 
        :param down: 
        :param headroom: 
        :param is_enabled: 
        :param labels: 

        :schema: DockerSwarmAutoScale
        '''
        if isinstance(down, dict):
            down = AutoScaleDown(**down)
        if isinstance(headroom, dict):
            headroom = Headroom(**headroom)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f417a27165b638fad84a8a1385c18ec8f7d05ac162ea2b393e73109b8de96de8)
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument down", value=down, expected_type=type_hints["down"])
            check_type(argname="argument headroom", value=headroom, expected_type=type_hints["headroom"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if down is not None:
            self._values["down"] = down
        if headroom is not None:
            self._values["headroom"] = headroom
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: DockerSwarmAutoScale#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def down(self) -> typing.Optional[AutoScaleDown]:
        '''
        :schema: DockerSwarmAutoScale#down
        '''
        result = self._values.get("down")
        return typing.cast(typing.Optional[AutoScaleDown], result)

    @builtins.property
    def headroom(self) -> typing.Optional["Headroom"]:
        '''
        :schema: DockerSwarmAutoScale#headroom
        '''
        result = self._values.get("headroom")
        return typing.cast(typing.Optional["Headroom"], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DockerSwarmAutoScale#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[Attribute]]:
        '''
        :schema: DockerSwarmAutoScale#labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[Attribute]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerSwarmAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Ecs",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scale": "autoScale",
        "batch": "batch",
        "cluster_name": "clusterName",
        "optimize_images": "optimizeImages",
    },
)
class Ecs:
    def __init__(
        self,
        *,
        auto_scale: typing.Optional[typing.Union["EcsAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        batch: typing.Optional[typing.Union["EcsBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        optimize_images: typing.Optional[typing.Union["EcsOptimizeImages", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_scale: 
        :param batch: 
        :param cluster_name: 
        :param optimize_images: 

        :schema: Ecs
        '''
        if isinstance(auto_scale, dict):
            auto_scale = EcsAutoScale(**auto_scale)
        if isinstance(batch, dict):
            batch = EcsBatch(**batch)
        if isinstance(optimize_images, dict):
            optimize_images = EcsOptimizeImages(**optimize_images)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466b61f9eb0052a5d9d806629bab4e13e48e193ee86a917a331cf4ad3efe11b0)
            check_type(argname="argument auto_scale", value=auto_scale, expected_type=type_hints["auto_scale"])
            check_type(argname="argument batch", value=batch, expected_type=type_hints["batch"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument optimize_images", value=optimize_images, expected_type=type_hints["optimize_images"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scale is not None:
            self._values["auto_scale"] = auto_scale
        if batch is not None:
            self._values["batch"] = batch
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if optimize_images is not None:
            self._values["optimize_images"] = optimize_images

    @builtins.property
    def auto_scale(self) -> typing.Optional["EcsAutoScale"]:
        '''
        :schema: Ecs#autoScale
        '''
        result = self._values.get("auto_scale")
        return typing.cast(typing.Optional["EcsAutoScale"], result)

    @builtins.property
    def batch(self) -> typing.Optional["EcsBatch"]:
        '''
        :schema: Ecs#batch
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional["EcsBatch"], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Ecs#clusterName
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optimize_images(self) -> typing.Optional["EcsOptimizeImages"]:
        '''
        :schema: Ecs#optimizeImages
        '''
        result = self._values.get("optimize_images")
        return typing.cast(typing.Optional["EcsOptimizeImages"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.EcsAutoScale",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "cooldown": "cooldown",
        "down": "down",
        "headroom": "headroom",
        "is_auto_config": "isAutoConfig",
        "is_enabled": "isEnabled",
        "should_scale_down_non_service_tasks": "shouldScaleDownNonServiceTasks",
    },
)
class EcsAutoScale:
    def __init__(
        self,
        *,
        attributes: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
        cooldown: typing.Optional[jsii.Number] = None,
        down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
        headroom: typing.Optional[typing.Union["Headroom", typing.Dict[builtins.str, typing.Any]]] = None,
        is_auto_config: typing.Optional[builtins.bool] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
        should_scale_down_non_service_tasks: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param attributes: 
        :param cooldown: 
        :param down: 
        :param headroom: 
        :param is_auto_config: 
        :param is_enabled: 
        :param should_scale_down_non_service_tasks: 

        :schema: EcsAutoScale
        '''
        if isinstance(down, dict):
            down = AutoScaleDown(**down)
        if isinstance(headroom, dict):
            headroom = Headroom(**headroom)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960c14eaf1e43efcff09a331d7e0c8ca3f5d02188737bb2497e50d7975d15f03)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument down", value=down, expected_type=type_hints["down"])
            check_type(argname="argument headroom", value=headroom, expected_type=type_hints["headroom"])
            check_type(argname="argument is_auto_config", value=is_auto_config, expected_type=type_hints["is_auto_config"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument should_scale_down_non_service_tasks", value=should_scale_down_non_service_tasks, expected_type=type_hints["should_scale_down_non_service_tasks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attributes is not None:
            self._values["attributes"] = attributes
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if down is not None:
            self._values["down"] = down
        if headroom is not None:
            self._values["headroom"] = headroom
        if is_auto_config is not None:
            self._values["is_auto_config"] = is_auto_config
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if should_scale_down_non_service_tasks is not None:
            self._values["should_scale_down_non_service_tasks"] = should_scale_down_non_service_tasks

    @builtins.property
    def attributes(self) -> typing.Optional[typing.List[Attribute]]:
        '''
        :schema: EcsAutoScale#attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.List[Attribute]], result)

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: EcsAutoScale#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def down(self) -> typing.Optional[AutoScaleDown]:
        '''
        :schema: EcsAutoScale#down
        '''
        result = self._values.get("down")
        return typing.cast(typing.Optional[AutoScaleDown], result)

    @builtins.property
    def headroom(self) -> typing.Optional["Headroom"]:
        '''
        :schema: EcsAutoScale#headroom
        '''
        result = self._values.get("headroom")
        return typing.cast(typing.Optional["Headroom"], result)

    @builtins.property
    def is_auto_config(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: EcsAutoScale#isAutoConfig
        '''
        result = self._values.get("is_auto_config")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: EcsAutoScale#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def should_scale_down_non_service_tasks(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: EcsAutoScale#shouldScaleDownNonServiceTasks
        '''
        result = self._values.get("should_scale_down_non_service_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.EcsBatch",
    jsii_struct_bases=[],
    name_mapping={"job_queue_names": "jobQueueNames"},
)
class EcsBatch:
    def __init__(
        self,
        *,
        job_queue_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param job_queue_names: 

        :schema: EcsBatch
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3264a75640a8edad557155e40074f9fd12451cf509ae5a20917902a0e1042b1)
            check_type(argname="argument job_queue_names", value=job_queue_names, expected_type=type_hints["job_queue_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_queue_names is not None:
            self._values["job_queue_names"] = job_queue_names

    @builtins.property
    def job_queue_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: EcsBatch#jobQueueNames
        '''
        result = self._values.get("job_queue_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.EcsOptimizeImages",
    jsii_struct_bases=[],
    name_mapping={
        "perform_at": "performAt",
        "should_optimize_ecs_ami": "shouldOptimizeEcsAmi",
        "time_windows": "timeWindows",
    },
)
class EcsOptimizeImages:
    def __init__(
        self,
        *,
        perform_at: typing.Optional[builtins.str] = None,
        should_optimize_ecs_ami: typing.Optional[builtins.bool] = None,
        time_windows: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param perform_at: 
        :param should_optimize_ecs_ami: 
        :param time_windows: 

        :schema: EcsOptimizeImages
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f70955dc6486d6e50bba46be0b08edd3f15932703fda1aab9edd609df0a9e38)
            check_type(argname="argument perform_at", value=perform_at, expected_type=type_hints["perform_at"])
            check_type(argname="argument should_optimize_ecs_ami", value=should_optimize_ecs_ami, expected_type=type_hints["should_optimize_ecs_ami"])
            check_type(argname="argument time_windows", value=time_windows, expected_type=type_hints["time_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if perform_at is not None:
            self._values["perform_at"] = perform_at
        if should_optimize_ecs_ami is not None:
            self._values["should_optimize_ecs_ami"] = should_optimize_ecs_ami
        if time_windows is not None:
            self._values["time_windows"] = time_windows

    @builtins.property
    def perform_at(self) -> typing.Optional[builtins.str]:
        '''
        :schema: EcsOptimizeImages#performAt
        '''
        result = self._values.get("perform_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def should_optimize_ecs_ami(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: EcsOptimizeImages#shouldOptimizeEcsAmi
        '''
        result = self._values.get("should_optimize_ecs_ami")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def time_windows(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: EcsOptimizeImages#timeWindows
        '''
        result = self._values.get("time_windows")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsOptimizeImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Headroom",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_per_unit": "cpuPerUnit",
        "memory_per_unit": "memoryPerUnit",
        "num_of_units": "numOfUnits",
    },
)
class Headroom:
    def __init__(
        self,
        *,
        cpu_per_unit: typing.Optional[jsii.Number] = None,
        memory_per_unit: typing.Optional[jsii.Number] = None,
        num_of_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_per_unit: 
        :param memory_per_unit: 
        :param num_of_units: 

        :schema: Headroom
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e986fe251c74bfbb246d8a4b74d8a3e00fc39a66b560a75d2d1b1d54c3cacc0c)
            check_type(argname="argument cpu_per_unit", value=cpu_per_unit, expected_type=type_hints["cpu_per_unit"])
            check_type(argname="argument memory_per_unit", value=memory_per_unit, expected_type=type_hints["memory_per_unit"])
            check_type(argname="argument num_of_units", value=num_of_units, expected_type=type_hints["num_of_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_per_unit is not None:
            self._values["cpu_per_unit"] = cpu_per_unit
        if memory_per_unit is not None:
            self._values["memory_per_unit"] = memory_per_unit
        if num_of_units is not None:
            self._values["num_of_units"] = num_of_units

    @builtins.property
    def cpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Headroom#cpuPerUnit
        '''
        result = self._values.get("cpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_per_unit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Headroom#memoryPerUnit
        '''
        result = self._values.get("memory_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_of_units(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Headroom#numOfUnits
        '''
        result = self._values.get("num_of_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Headroom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Kubernetes",
    jsii_struct_bases=[],
    name_mapping={
        "api_server": "apiServer",
        "auto_scale": "autoScale",
        "cluster_identifier": "clusterIdentifier",
        "integration_mode": "integrationMode",
        "token": "token",
    },
)
class Kubernetes:
    def __init__(
        self,
        *,
        api_server: typing.Optional[builtins.str] = None,
        auto_scale: typing.Optional[typing.Union["KubernetesAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        integration_mode: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_server: 
        :param auto_scale: 
        :param cluster_identifier: 
        :param integration_mode: 
        :param token: 

        :schema: Kubernetes
        '''
        if isinstance(auto_scale, dict):
            auto_scale = KubernetesAutoScale(**auto_scale)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3694c1c971f6eb09e76cd892ae70e4ce646c4ef0d7dabbf961ffb6d9e2373ef)
            check_type(argname="argument api_server", value=api_server, expected_type=type_hints["api_server"])
            check_type(argname="argument auto_scale", value=auto_scale, expected_type=type_hints["auto_scale"])
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument integration_mode", value=integration_mode, expected_type=type_hints["integration_mode"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_server is not None:
            self._values["api_server"] = api_server
        if auto_scale is not None:
            self._values["auto_scale"] = auto_scale
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if integration_mode is not None:
            self._values["integration_mode"] = integration_mode
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def api_server(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Kubernetes#apiServer
        '''
        result = self._values.get("api_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_scale(self) -> typing.Optional["KubernetesAutoScale"]:
        '''
        :schema: Kubernetes#autoScale
        '''
        result = self._values.get("auto_scale")
        return typing.cast(typing.Optional["KubernetesAutoScale"], result)

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Kubernetes#clusterIdentifier
        '''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_mode(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Kubernetes#integrationMode
        '''
        result = self._values.get("integration_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Kubernetes#token
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Kubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.KubernetesAutoScale",
    jsii_struct_bases=[],
    name_mapping={
        "cooldown": "cooldown",
        "down": "down",
        "headroom": "headroom",
        "is_auto_config": "isAutoConfig",
        "is_enabled": "isEnabled",
        "labels": "labels",
        "resource_limits": "resourceLimits",
    },
)
class KubernetesAutoScale:
    def __init__(
        self,
        *,
        cooldown: typing.Optional[jsii.Number] = None,
        down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
        headroom: typing.Optional[typing.Union["KubernetesAutoScaleHeadroom", typing.Dict[builtins.str, typing.Any]]] = None,
        is_auto_config: typing.Optional[builtins.bool] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_limits: typing.Optional[typing.Union["KubernetesAutoScaleResourceLimits", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cooldown: 
        :param down: 
        :param headroom: 
        :param is_auto_config: 
        :param is_enabled: 
        :param labels: 
        :param resource_limits: 

        :schema: KubernetesAutoScale
        '''
        if isinstance(down, dict):
            down = AutoScaleDown(**down)
        if isinstance(headroom, dict):
            headroom = KubernetesAutoScaleHeadroom(**headroom)
        if isinstance(resource_limits, dict):
            resource_limits = KubernetesAutoScaleResourceLimits(**resource_limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f111c1c7e1dc537f7e0ede4e5c37c764ed66451e0a389a806d69a95b886162c)
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument down", value=down, expected_type=type_hints["down"])
            check_type(argname="argument headroom", value=headroom, expected_type=type_hints["headroom"])
            check_type(argname="argument is_auto_config", value=is_auto_config, expected_type=type_hints["is_auto_config"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument resource_limits", value=resource_limits, expected_type=type_hints["resource_limits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if down is not None:
            self._values["down"] = down
        if headroom is not None:
            self._values["headroom"] = headroom
        if is_auto_config is not None:
            self._values["is_auto_config"] = is_auto_config
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if labels is not None:
            self._values["labels"] = labels
        if resource_limits is not None:
            self._values["resource_limits"] = resource_limits

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScale#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def down(self) -> typing.Optional[AutoScaleDown]:
        '''
        :schema: KubernetesAutoScale#down
        '''
        result = self._values.get("down")
        return typing.cast(typing.Optional[AutoScaleDown], result)

    @builtins.property
    def headroom(self) -> typing.Optional["KubernetesAutoScaleHeadroom"]:
        '''
        :schema: KubernetesAutoScale#headroom
        '''
        result = self._values.get("headroom")
        return typing.cast(typing.Optional["KubernetesAutoScaleHeadroom"], result)

    @builtins.property
    def is_auto_config(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: KubernetesAutoScale#isAutoConfig
        '''
        result = self._values.get("is_auto_config")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: KubernetesAutoScale#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[Attribute]]:
        '''
        :schema: KubernetesAutoScale#labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[Attribute]], result)

    @builtins.property
    def resource_limits(self) -> typing.Optional["KubernetesAutoScaleResourceLimits"]:
        '''
        :schema: KubernetesAutoScale#resourceLimits
        '''
        result = self._values.get("resource_limits")
        return typing.cast(typing.Optional["KubernetesAutoScaleResourceLimits"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.KubernetesAutoScaleHeadroom",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_per_unit": "cpuPerUnit",
        "gpu_per_unit": "gpuPerUnit",
        "memory_per_unit": "memoryPerUnit",
        "num_of_units": "numOfUnits",
    },
)
class KubernetesAutoScaleHeadroom:
    def __init__(
        self,
        *,
        cpu_per_unit: typing.Optional[jsii.Number] = None,
        gpu_per_unit: typing.Optional[jsii.Number] = None,
        memory_per_unit: typing.Optional[jsii.Number] = None,
        num_of_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_per_unit: 
        :param gpu_per_unit: 
        :param memory_per_unit: 
        :param num_of_units: 

        :schema: KubernetesAutoScaleHeadroom
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72787ca4b189c23e71172780dc61cd9da82ae53326c4a729fa374904c8c57bb7)
            check_type(argname="argument cpu_per_unit", value=cpu_per_unit, expected_type=type_hints["cpu_per_unit"])
            check_type(argname="argument gpu_per_unit", value=gpu_per_unit, expected_type=type_hints["gpu_per_unit"])
            check_type(argname="argument memory_per_unit", value=memory_per_unit, expected_type=type_hints["memory_per_unit"])
            check_type(argname="argument num_of_units", value=num_of_units, expected_type=type_hints["num_of_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_per_unit is not None:
            self._values["cpu_per_unit"] = cpu_per_unit
        if gpu_per_unit is not None:
            self._values["gpu_per_unit"] = gpu_per_unit
        if memory_per_unit is not None:
            self._values["memory_per_unit"] = memory_per_unit
        if num_of_units is not None:
            self._values["num_of_units"] = num_of_units

    @builtins.property
    def cpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScaleHeadroom#cpuPerUnit
        '''
        result = self._values.get("cpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScaleHeadroom#gpuPerUnit
        '''
        result = self._values.get("gpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_per_unit(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScaleHeadroom#memoryPerUnit
        '''
        result = self._values.get("memory_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_of_units(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScaleHeadroom#numOfUnits
        '''
        result = self._values.get("num_of_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesAutoScaleHeadroom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.KubernetesAutoScaleResourceLimits",
    jsii_struct_bases=[],
    name_mapping={"max_memory_gib": "maxMemoryGib", "max_v_cpu": "maxVCpu"},
)
class KubernetesAutoScaleResourceLimits:
    def __init__(
        self,
        *,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_v_cpu: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_memory_gib: 
        :param max_v_cpu: 

        :schema: KubernetesAutoScaleResourceLimits
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb9de9d51f10b20b02ef3faf61d8fcf4cec38df4a7fc9da3d3cd842ac881e3a)
            check_type(argname="argument max_memory_gib", value=max_memory_gib, expected_type=type_hints["max_memory_gib"])
            check_type(argname="argument max_v_cpu", value=max_v_cpu, expected_type=type_hints["max_v_cpu"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_memory_gib is not None:
            self._values["max_memory_gib"] = max_memory_gib
        if max_v_cpu is not None:
            self._values["max_v_cpu"] = max_v_cpu

    @builtins.property
    def max_memory_gib(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScaleResourceLimits#maxMemoryGib
        '''
        result = self._values.get("max_memory_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_v_cpu(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: KubernetesAutoScaleResourceLimits#maxVCpu
        '''
        result = self._values.get("max_v_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesAutoScaleResourceLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.LoadBalancerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "auto_weight": "autoWeight",
        "az_awareness": "azAwareness",
        "balancer_id": "balancerId",
        "name": "name",
        "target_set_id": "targetSetId",
        "type": "type",
    },
)
class LoadBalancerConfig:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        auto_weight: typing.Optional[builtins.bool] = None,
        az_awareness: typing.Optional[builtins.bool] = None,
        balancer_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        target_set_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: 
        :param auto_weight: 
        :param az_awareness: 
        :param balancer_id: 
        :param name: 
        :param target_set_id: 
        :param type: 

        :schema: LoadBalancerConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9853541fd4fef1f9d5344d4945aeacdf8670627a72a96d335c0acce346368f)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument auto_weight", value=auto_weight, expected_type=type_hints["auto_weight"])
            check_type(argname="argument az_awareness", value=az_awareness, expected_type=type_hints["az_awareness"])
            check_type(argname="argument balancer_id", value=balancer_id, expected_type=type_hints["balancer_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target_set_id", value=target_set_id, expected_type=type_hints["target_set_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if auto_weight is not None:
            self._values["auto_weight"] = auto_weight
        if az_awareness is not None:
            self._values["az_awareness"] = az_awareness
        if balancer_id is not None:
            self._values["balancer_id"] = balancer_id
        if name is not None:
            self._values["name"] = name
        if target_set_id is not None:
            self._values["target_set_id"] = target_set_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: LoadBalancerConfig#arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_weight(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: LoadBalancerConfig#autoWeight
        '''
        result = self._values.get("auto_weight")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def az_awareness(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: LoadBalancerConfig#azAwareness
        '''
        result = self._values.get("az_awareness")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def balancer_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: LoadBalancerConfig#balancerId
        '''
        result = self._values.get("balancer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: LoadBalancerConfig#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_set_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: LoadBalancerConfig#targetSetId
        '''
        result = self._values.get("target_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: LoadBalancerConfig#type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.LoadBalancersConfig",
    jsii_struct_bases=[],
    name_mapping={"load_balancers": "loadBalancers"},
)
class LoadBalancersConfig:
    def __init__(
        self,
        *,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param load_balancers: 

        :schema: LoadBalancersConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74bf1ac7dbb4658a198d974ee4ed79843672d1e3e7cd2943545bcf9286fe236)
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List[LoadBalancerConfig]]:
        '''
        :schema: LoadBalancersConfig#loadBalancers
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[LoadBalancerConfig]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Nomad",
    jsii_struct_bases=[],
    name_mapping={
        "acl_token": "aclToken",
        "auto_scale": "autoScale",
        "master_host": "masterHost",
        "master_port": "masterPort",
        "tls_config": "tlsConfig",
    },
)
class Nomad:
    def __init__(
        self,
        *,
        acl_token: typing.Optional[builtins.str] = None,
        auto_scale: typing.Optional[typing.Union["NomadAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        master_host: typing.Optional[builtins.str] = None,
        master_port: typing.Optional[jsii.Number] = None,
        tls_config: typing.Optional[typing.Union["TlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acl_token: 
        :param auto_scale: 
        :param master_host: 
        :param master_port: 
        :param tls_config: 

        :schema: Nomad
        '''
        if isinstance(auto_scale, dict):
            auto_scale = NomadAutoScale(**auto_scale)
        if isinstance(tls_config, dict):
            tls_config = TlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9b3422a120172edbe3288a42b94079fe1e021790658ce6faa7a8cf1b5e0729)
            check_type(argname="argument acl_token", value=acl_token, expected_type=type_hints["acl_token"])
            check_type(argname="argument auto_scale", value=auto_scale, expected_type=type_hints["auto_scale"])
            check_type(argname="argument master_host", value=master_host, expected_type=type_hints["master_host"])
            check_type(argname="argument master_port", value=master_port, expected_type=type_hints["master_port"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acl_token is not None:
            self._values["acl_token"] = acl_token
        if auto_scale is not None:
            self._values["auto_scale"] = auto_scale
        if master_host is not None:
            self._values["master_host"] = master_host
        if master_port is not None:
            self._values["master_port"] = master_port
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def acl_token(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Nomad#aclToken
        '''
        result = self._values.get("acl_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_scale(self) -> typing.Optional["NomadAutoScale"]:
        '''
        :schema: Nomad#autoScale
        '''
        result = self._values.get("auto_scale")
        return typing.cast(typing.Optional["NomadAutoScale"], result)

    @builtins.property
    def master_host(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Nomad#masterHost
        '''
        result = self._values.get("master_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_port(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Nomad#masterPort
        '''
        result = self._values.get("master_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_config(self) -> typing.Optional["TlsConfig"]:
        '''
        :schema: Nomad#tlsConfig
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["TlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Nomad(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.NomadAutoScale",
    jsii_struct_bases=[],
    name_mapping={
        "constraints": "constraints",
        "cooldown": "cooldown",
        "down": "down",
        "headroom": "headroom",
        "is_auto_config": "isAutoConfig",
        "is_enabled": "isEnabled",
    },
)
class NomadAutoScale:
    def __init__(
        self,
        *,
        constraints: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
        cooldown: typing.Optional[jsii.Number] = None,
        down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
        headroom: typing.Optional[typing.Union[Headroom, typing.Dict[builtins.str, typing.Any]]] = None,
        is_auto_config: typing.Optional[builtins.bool] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param constraints: 
        :param cooldown: 
        :param down: 
        :param headroom: 
        :param is_auto_config: 
        :param is_enabled: 

        :schema: NomadAutoScale
        '''
        if isinstance(down, dict):
            down = AutoScaleDown(**down)
        if isinstance(headroom, dict):
            headroom = Headroom(**headroom)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45064f0f945dd7cde95702d7ae27abd708fb99e80a05f88db7834b22dbf3e29)
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument down", value=down, expected_type=type_hints["down"])
            check_type(argname="argument headroom", value=headroom, expected_type=type_hints["headroom"])
            check_type(argname="argument is_auto_config", value=is_auto_config, expected_type=type_hints["is_auto_config"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if constraints is not None:
            self._values["constraints"] = constraints
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if down is not None:
            self._values["down"] = down
        if headroom is not None:
            self._values["headroom"] = headroom
        if is_auto_config is not None:
            self._values["is_auto_config"] = is_auto_config
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled

    @builtins.property
    def constraints(self) -> typing.Optional[typing.List[Attribute]]:
        '''
        :schema: NomadAutoScale#constraints
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Optional[typing.List[Attribute]], result)

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: NomadAutoScale#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def down(self) -> typing.Optional[AutoScaleDown]:
        '''
        :schema: NomadAutoScale#down
        '''
        result = self._values.get("down")
        return typing.cast(typing.Optional[AutoScaleDown], result)

    @builtins.property
    def headroom(self) -> typing.Optional[Headroom]:
        '''
        :schema: NomadAutoScale#headroom
        '''
        result = self._values.get("headroom")
        return typing.cast(typing.Optional[Headroom], result)

    @builtins.property
    def is_auto_config(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: NomadAutoScale#isAutoConfig
        '''
        result = self._values.get("is_auto_config")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: NomadAutoScale#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NomadAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ResourceRequirement",
    jsii_struct_bases=[],
    name_mapping={"maximum": "maximum", "minimum": "minimum"},
)
class ResourceRequirement:
    def __init__(
        self,
        *,
        maximum: typing.Optional[jsii.Number] = None,
        minimum: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum: 
        :param minimum: 

        :schema: ResourceRequirement
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ed0d055209a39f79c800529c0286604f73899b0184585dc587389d4f4c56a6)
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum

    @builtins.property
    def maximum(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ResourceRequirement#maximum
        '''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ResourceRequirement#minimum
        '''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ResourceTagSpecificationConfig",
    jsii_struct_bases=[],
    name_mapping={"should_tag": "shouldTag"},
)
class ResourceTagSpecificationConfig:
    def __init__(self, *, should_tag: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param should_tag: 

        :schema: ResourceTagSpecificationConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b96f5d6f4798f6a974636f73901548e6462df4f6adbf041e83640fa78855d89)
            check_type(argname="argument should_tag", value=should_tag, expected_type=type_hints["should_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if should_tag is not None:
            self._values["should_tag"] = should_tag

    @builtins.property
    def should_tag(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: ResourceTagSpecificationConfig#shouldTag
        '''
        result = self._values.get("should_tag")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceTagSpecificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScaleDownAction",
    jsii_struct_bases=[],
    name_mapping={
        "maximum": "maximum",
        "minimum": "minimum",
        "target": "target",
        "type": "type",
    },
)
class ScaleDownAction:
    def __init__(
        self,
        *,
        maximum: typing.Optional[builtins.str] = None,
        minimum: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum: 
        :param minimum: 
        :param target: 
        :param type: 

        :schema: ScaleDownAction
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48233f1f1ee03947b62a946b093370816c851996acca56d85938f26c74edff44)
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum
        if target is not None:
            self._values["target"] = target
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def maximum(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleDownAction#maximum
        '''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleDownAction#minimum
        '''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleDownAction#target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleDownAction#type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScaleDownAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScaleDownStepAdjustment",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "threshold": "threshold"},
)
class ScaleDownStepAdjustment:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[ScaleDownAction, typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: 
        :param threshold: 

        :schema: ScaleDownStepAdjustment
        '''
        if isinstance(action, dict):
            action = ScaleDownAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a501ac3f74b4caa1a7827f6067dbe447c02fed3f7b7806cb6b8962d7ff1d68)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def action(self) -> typing.Optional[ScaleDownAction]:
        '''
        :schema: ScaleDownStepAdjustment#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[ScaleDownAction], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScaleDownStepAdjustment#threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScaleDownStepAdjustment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScaleUpAction",
    jsii_struct_bases=[],
    name_mapping={
        "maximum": "maximum",
        "minimum": "minimum",
        "target": "target",
        "type": "type",
    },
)
class ScaleUpAction:
    def __init__(
        self,
        *,
        maximum: typing.Optional[builtins.str] = None,
        minimum: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum: 
        :param minimum: 
        :param target: 
        :param type: 

        :schema: ScaleUpAction
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fa7250c0bf2ffa7dcc325e846e7b40a28449aa3f280f17cbc7435179e2c60b)
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum
        if target is not None:
            self._values["target"] = target
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def maximum(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleUpAction#maximum
        '''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleUpAction#minimum
        '''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleUpAction#target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScaleUpAction#type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScaleUpAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScaleUpStepAdjustment",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "threshold": "threshold"},
)
class ScaleUpStepAdjustment:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[ScaleUpAction, typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: 
        :param threshold: 

        :schema: ScaleUpStepAdjustment
        '''
        if isinstance(action, dict):
            action = ScaleUpAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc497ef3fd9fbcbdfeda2c543fabd663139f6e3aadf169885a467d779e809261)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def action(self) -> typing.Optional[ScaleUpAction]:
        '''
        :schema: ScaleUpStepAdjustment#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[ScaleUpAction], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScaleUpStepAdjustment#threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScaleUpStepAdjustment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScalingDownPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "cooldown": "cooldown",
        "dimension": "dimension",
        "evaluation_periods": "evaluationPeriods",
        "extended_statistic": "extendedStatistic",
        "is_enabled": "isEnabled",
        "metric_name": "metricName",
        "namespace": "namespace",
        "operator": "operator",
        "period": "period",
        "policy_name": "policyName",
        "source": "source",
        "statistic": "statistic",
        "step_adjustments": "stepAdjustments",
        "threshold": "threshold",
        "unit": "unit",
    },
)
class ScalingDownPolicy:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[ScaleDownAction, typing.Dict[builtins.str, typing.Any]]] = None,
        cooldown: typing.Optional[jsii.Number] = None,
        dimension: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
        metric_name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        period: typing.Optional[jsii.Number] = None,
        policy_name: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        step_adjustments: typing.Optional[typing.Sequence[typing.Union[ScaleDownStepAdjustment, typing.Dict[builtins.str, typing.Any]]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: 
        :param cooldown: 
        :param dimension: 
        :param evaluation_periods: 
        :param extended_statistic: 
        :param is_enabled: 
        :param metric_name: 
        :param namespace: 
        :param operator: 
        :param period: 
        :param policy_name: 
        :param source: 
        :param statistic: 
        :param step_adjustments: 
        :param threshold: 
        :param unit: 

        :schema: ScalingDownPolicy
        '''
        if isinstance(action, dict):
            action = ScaleDownAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437cfe3caf825521b8a4e6b8b4c80e37560c4229b3945d66ad4e288b56ddac4f)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument extended_statistic", value=extended_statistic, expected_type=type_hints["extended_statistic"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument step_adjustments", value=step_adjustments, expected_type=type_hints["step_adjustments"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if dimension is not None:
            self._values["dimension"] = dimension
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if namespace is not None:
            self._values["namespace"] = namespace
        if operator is not None:
            self._values["operator"] = operator
        if period is not None:
            self._values["period"] = period
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if source is not None:
            self._values["source"] = source
        if statistic is not None:
            self._values["statistic"] = statistic
        if step_adjustments is not None:
            self._values["step_adjustments"] = step_adjustments
        if threshold is not None:
            self._values["threshold"] = threshold
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def action(self) -> typing.Optional[ScaleDownAction]:
        '''
        :schema: ScalingDownPolicy#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[ScaleDownAction], result)

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingDownPolicy#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dimension(self) -> typing.Optional[typing.List[Dimension]]:
        '''
        :schema: ScalingDownPolicy#dimension
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.List[Dimension]], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingDownPolicy#evaluationPeriods
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#extendedStatistic
        '''
        result = self._values.get("extended_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: ScalingDownPolicy#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#metricName
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#operator
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingDownPolicy#period
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#policyName
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def step_adjustments(self) -> typing.Optional[typing.List[ScaleDownStepAdjustment]]:
        '''
        :schema: ScalingDownPolicy#stepAdjustments
        '''
        result = self._values.get("step_adjustments")
        return typing.cast(typing.Optional[typing.List[ScaleDownStepAdjustment]], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingDownPolicy#threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingDownPolicy#unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalingDownPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScalingTargetPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cooldown": "cooldown",
        "dimension": "dimension",
        "evaluation_periods": "evaluationPeriods",
        "max_capacity_per_scale": "maxCapacityPerScale",
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "policy_name": "policyName",
        "predictive": "predictive",
        "source": "source",
        "statistic": "statistic",
        "target": "target",
        "unit": "unit",
    },
)
class ScalingTargetPolicy:
    def __init__(
        self,
        *,
        cooldown: typing.Optional[jsii.Number] = None,
        dimension: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        max_capacity_per_scale: typing.Optional[builtins.str] = None,
        metric_name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        period: typing.Optional[jsii.Number] = None,
        policy_name: typing.Optional[builtins.str] = None,
        predictive: typing.Optional[typing.Union["ScalingTargetPolicyPredictive", typing.Dict[builtins.str, typing.Any]]] = None,
        source: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        target: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooldown: 
        :param dimension: 
        :param evaluation_periods: 
        :param max_capacity_per_scale: 
        :param metric_name: 
        :param namespace: 
        :param period: 
        :param policy_name: 
        :param predictive: 
        :param source: 
        :param statistic: 
        :param target: 
        :param unit: 

        :schema: ScalingTargetPolicy
        '''
        if isinstance(predictive, dict):
            predictive = ScalingTargetPolicyPredictive(**predictive)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8c641bcf497af93b386b851070f78445dc10e5b6c7f72d7c7d7a9d5cb49f47)
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument max_capacity_per_scale", value=max_capacity_per_scale, expected_type=type_hints["max_capacity_per_scale"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument predictive", value=predictive, expected_type=type_hints["predictive"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if dimension is not None:
            self._values["dimension"] = dimension
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if max_capacity_per_scale is not None:
            self._values["max_capacity_per_scale"] = max_capacity_per_scale
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if namespace is not None:
            self._values["namespace"] = namespace
        if period is not None:
            self._values["period"] = period
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if predictive is not None:
            self._values["predictive"] = predictive
        if source is not None:
            self._values["source"] = source
        if statistic is not None:
            self._values["statistic"] = statistic
        if target is not None:
            self._values["target"] = target
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingTargetPolicy#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dimension(self) -> typing.Optional[typing.List[Dimension]]:
        '''
        :schema: ScalingTargetPolicy#dimension
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.List[Dimension]], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingTargetPolicy#evaluationPeriods
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_capacity_per_scale(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#maxCapacityPerScale
        '''
        result = self._values.get("max_capacity_per_scale")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#metricName
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingTargetPolicy#period
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#policyName
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predictive(self) -> typing.Optional["ScalingTargetPolicyPredictive"]:
        '''
        :schema: ScalingTargetPolicy#predictive
        '''
        result = self._values.get("predictive")
        return typing.cast(typing.Optional["ScalingTargetPolicyPredictive"], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingTargetPolicy#target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicy#unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalingTargetPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScalingTargetPolicyPredictive",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class ScalingTargetPolicyPredictive:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: 

        :schema: ScalingTargetPolicyPredictive
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ddc90adc76ff6fc7505c5219d0dd35decd6a46991a5f95ad01ba57b174313c)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingTargetPolicyPredictive#mode
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalingTargetPolicyPredictive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.ScalingUpPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "cooldown": "cooldown",
        "dimension": "dimension",
        "evaluation_periods": "evaluationPeriods",
        "extended_statistic": "extendedStatistic",
        "is_enabled": "isEnabled",
        "metric_name": "metricName",
        "namespace": "namespace",
        "operator": "operator",
        "period": "period",
        "policy_name": "policyName",
        "should_resume_stateful": "shouldResumeStateful",
        "source": "source",
        "statistic": "statistic",
        "step_adjustments": "stepAdjustments",
        "threshold": "threshold",
        "unit": "unit",
    },
)
class ScalingUpPolicy:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[ScaleUpAction, typing.Dict[builtins.str, typing.Any]]] = None,
        cooldown: typing.Optional[jsii.Number] = None,
        dimension: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
        metric_name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        period: typing.Optional[jsii.Number] = None,
        policy_name: typing.Optional[builtins.str] = None,
        should_resume_stateful: typing.Optional[builtins.bool] = None,
        source: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        step_adjustments: typing.Optional[typing.Sequence[typing.Union[ScaleUpStepAdjustment, typing.Dict[builtins.str, typing.Any]]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: 
        :param cooldown: 
        :param dimension: 
        :param evaluation_periods: 
        :param extended_statistic: 
        :param is_enabled: 
        :param metric_name: 
        :param namespace: 
        :param operator: 
        :param period: 
        :param policy_name: 
        :param should_resume_stateful: 
        :param source: 
        :param statistic: 
        :param step_adjustments: 
        :param threshold: 
        :param unit: 

        :schema: ScalingUpPolicy
        '''
        if isinstance(action, dict):
            action = ScaleUpAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ce11ffeeda21d567628540e9dd295211ef4ccbcd8dab40741388e140cfffbf)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument extended_statistic", value=extended_statistic, expected_type=type_hints["extended_statistic"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument should_resume_stateful", value=should_resume_stateful, expected_type=type_hints["should_resume_stateful"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument step_adjustments", value=step_adjustments, expected_type=type_hints["step_adjustments"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if dimension is not None:
            self._values["dimension"] = dimension
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if namespace is not None:
            self._values["namespace"] = namespace
        if operator is not None:
            self._values["operator"] = operator
        if period is not None:
            self._values["period"] = period
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if should_resume_stateful is not None:
            self._values["should_resume_stateful"] = should_resume_stateful
        if source is not None:
            self._values["source"] = source
        if statistic is not None:
            self._values["statistic"] = statistic
        if step_adjustments is not None:
            self._values["step_adjustments"] = step_adjustments
        if threshold is not None:
            self._values["threshold"] = threshold
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def action(self) -> typing.Optional[ScaleUpAction]:
        '''
        :schema: ScalingUpPolicy#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[ScaleUpAction], result)

    @builtins.property
    def cooldown(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingUpPolicy#cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dimension(self) -> typing.Optional[typing.List[Dimension]]:
        '''
        :schema: ScalingUpPolicy#dimension
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.List[Dimension]], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingUpPolicy#evaluationPeriods
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#extendedStatistic
        '''
        result = self._values.get("extended_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: ScalingUpPolicy#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#metricName
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#operator
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingUpPolicy#period
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#policyName
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def should_resume_stateful(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: ScalingUpPolicy#shouldResumeStateful
        '''
        result = self._values.get("should_resume_stateful")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def step_adjustments(self) -> typing.Optional[typing.List[ScaleUpStepAdjustment]]:
        '''
        :schema: ScalingUpPolicy#stepAdjustments
        '''
        result = self._values.get("step_adjustments")
        return typing.cast(typing.Optional[typing.List[ScaleUpStepAdjustment]], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScalingUpPolicy#threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScalingUpPolicy#unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalingUpPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Tag",
    jsii_struct_bases=[],
    name_mapping={"tag_key": "tagKey", "tag_value": "tagValue"},
)
class Tag:
    def __init__(
        self,
        *,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tag_key: 
        :param tag_value: 

        :schema: Tag
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba768e6ef5a62c63e7aadaf97eae5cb36a88ad2361f245b7acce6300e8b8674a)
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Tag#tagKey
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Tag#tagValue
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.Task",
    jsii_struct_bases=[],
    name_mapping={
        "adjustment": "adjustment",
        "adjustment_percentage": "adjustmentPercentage",
        "batch_size_percentage": "batchSizePercentage",
        "cron_expression": "cronExpression",
        "frequency": "frequency",
        "grace_period": "gracePeriod",
        "is_enabled": "isEnabled",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "scale_max_capacity": "scaleMaxCapacity",
        "scale_min_capacity": "scaleMinCapacity",
        "scale_target_capacity": "scaleTargetCapacity",
        "start_time": "startTime",
        "target_capacity": "targetCapacity",
        "task_type": "taskType",
    },
)
class Task:
    def __init__(
        self,
        *,
        adjustment: typing.Optional[jsii.Number] = None,
        adjustment_percentage: typing.Optional[jsii.Number] = None,
        batch_size_percentage: typing.Optional[jsii.Number] = None,
        cron_expression: typing.Optional[builtins.str] = None,
        frequency: typing.Optional[builtins.str] = None,
        grace_period: typing.Optional[jsii.Number] = None,
        is_enabled: typing.Optional[builtins.bool] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        scale_max_capacity: typing.Optional[jsii.Number] = None,
        scale_min_capacity: typing.Optional[jsii.Number] = None,
        scale_target_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        task_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param adjustment: 
        :param adjustment_percentage: 
        :param batch_size_percentage: 
        :param cron_expression: 
        :param frequency: 
        :param grace_period: 
        :param is_enabled: 
        :param max_capacity: 
        :param min_capacity: 
        :param scale_max_capacity: 
        :param scale_min_capacity: 
        :param scale_target_capacity: 
        :param start_time: 
        :param target_capacity: 
        :param task_type: 

        :schema: Task
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b6b735b15d3de623e7f51f851353aee987008f8fdb1a3dda95a881fe0689a7)
            check_type(argname="argument adjustment", value=adjustment, expected_type=type_hints["adjustment"])
            check_type(argname="argument adjustment_percentage", value=adjustment_percentage, expected_type=type_hints["adjustment_percentage"])
            check_type(argname="argument batch_size_percentage", value=batch_size_percentage, expected_type=type_hints["batch_size_percentage"])
            check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument grace_period", value=grace_period, expected_type=type_hints["grace_period"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument scale_max_capacity", value=scale_max_capacity, expected_type=type_hints["scale_max_capacity"])
            check_type(argname="argument scale_min_capacity", value=scale_min_capacity, expected_type=type_hints["scale_min_capacity"])
            check_type(argname="argument scale_target_capacity", value=scale_target_capacity, expected_type=type_hints["scale_target_capacity"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument target_capacity", value=target_capacity, expected_type=type_hints["target_capacity"])
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if adjustment is not None:
            self._values["adjustment"] = adjustment
        if adjustment_percentage is not None:
            self._values["adjustment_percentage"] = adjustment_percentage
        if batch_size_percentage is not None:
            self._values["batch_size_percentage"] = batch_size_percentage
        if cron_expression is not None:
            self._values["cron_expression"] = cron_expression
        if frequency is not None:
            self._values["frequency"] = frequency
        if grace_period is not None:
            self._values["grace_period"] = grace_period
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if scale_max_capacity is not None:
            self._values["scale_max_capacity"] = scale_max_capacity
        if scale_min_capacity is not None:
            self._values["scale_min_capacity"] = scale_min_capacity
        if scale_target_capacity is not None:
            self._values["scale_target_capacity"] = scale_target_capacity
        if start_time is not None:
            self._values["start_time"] = start_time
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if task_type is not None:
            self._values["task_type"] = task_type

    @builtins.property
    def adjustment(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#adjustment
        '''
        result = self._values.get("adjustment")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def adjustment_percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#adjustmentPercentage
        '''
        result = self._values.get("adjustment_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_size_percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#batchSizePercentage
        '''
        result = self._values.get("batch_size_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cron_expression(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Task#cronExpression
        '''
        result = self._values.get("cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Task#frequency
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grace_period(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#gracePeriod
        '''
        result = self._values.get("grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Task#isEnabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#maxCapacity
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#minCapacity
        '''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_max_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#scaleMaxCapacity
        '''
        result = self._values.get("scale_max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_min_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#scaleMinCapacity
        '''
        result = self._values.get("scale_min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_target_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#scaleTargetCapacity
        '''
        result = self._values.get("scale_target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Task#startTime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Task#targetCapacity
        '''
        result = self._values.get("target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Task#taskType
        '''
        result = self._values.get("task_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Task(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/spot-elastigroup-group.TlsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "private_key": "privateKey",
        "tls_enabled": "tlsEnabled",
    },
)
class TlsConfig:
    def __init__(
        self,
        *,
        certificate: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        tls_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param certificate: 
        :param private_key: 
        :param tls_enabled: 

        :schema: TlsConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3060f10fbd76d62a140badf76efdd51788d0e051b12ea2203b7a630389571221)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument tls_enabled", value=tls_enabled, expected_type=type_hints["tls_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if private_key is not None:
            self._values["private_key"] = private_key
        if tls_enabled is not None:
            self._values["tls_enabled"] = tls_enabled

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''
        :schema: TlsConfig#certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: TlsConfig#privateKey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: TlsConfig#tlsEnabled
        '''
        result = self._values.get("tls_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Attribute",
    "AutoScaleDown",
    "BeanStalkStrategy",
    "BlockDeviceMapping",
    "BlockDeviceMappingEbs",
    "BlockDeviceMappingEbsDynamicVolumeSize",
    "BlockDeviceMappingEbsVolumeType",
    "CfnGroup",
    "CfnGroupProps",
    "CfnGroupPropsCredentials",
    "CfnGroupPropsGroup",
    "CfnGroupPropsGroupCapacity",
    "CfnGroupPropsGroupCompute",
    "CfnGroupPropsGroupComputeAvailabilityZones",
    "CfnGroupPropsGroupComputeEbsVolumePool",
    "CfnGroupPropsGroupComputeInstanceTypes",
    "CfnGroupPropsGroupComputeInstanceTypesResourceRequirements",
    "CfnGroupPropsGroupComputeInstanceTypesWeights",
    "CfnGroupPropsGroupComputeLaunchSpecification",
    "CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions",
    "CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification",
    "CfnGroupPropsGroupComputeLaunchSpecificationIamRole",
    "CfnGroupPropsGroupComputeLaunchSpecificationImages",
    "CfnGroupPropsGroupComputeLaunchSpecificationItf",
    "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers",
    "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups",
    "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules",
    "CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups",
    "CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig",
    "CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher",
    "CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions",
    "CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces",
    "CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses",
    "CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification",
    "CfnGroupPropsGroupComputeVolumeAttachments",
    "CfnGroupPropsGroupComputeVolumeAttachmentsVolumes",
    "CfnGroupPropsGroupScaling",
    "CfnGroupPropsGroupScalingMultipleMetrics",
    "CfnGroupPropsGroupScalingMultipleMetricsExpressions",
    "CfnGroupPropsGroupScalingMultipleMetricsMetrics",
    "CfnGroupPropsGroupScheduling",
    "CfnGroupPropsGroupStrategy",
    "CfnGroupPropsGroupStrategyPersistence",
    "CfnGroupPropsGroupStrategyRevertToSpot",
    "CfnGroupPropsGroupStrategyScalingStrategy",
    "CfnGroupPropsGroupStrategySignals",
    "CfnGroupPropsGroupThirdPartiesIntegration",
    "CfnGroupPropsGroupThirdPartiesIntegrationChef",
    "CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy",
    "CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups",
    "CfnGroupPropsGroupThirdPartiesIntegrationDatadog",
    "CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport",
    "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk",
    "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences",
    "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions",
    "CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate",
    "CfnGroupPropsGroupThirdPartiesIntegrationGitlab",
    "CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner",
    "CfnGroupPropsGroupThirdPartiesIntegrationJenkins",
    "CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod",
    "CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp",
    "CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh",
    "CfnGroupPropsGroupThirdPartiesIntegrationMesosphere",
    "CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime",
    "CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks",
    "CfnGroupPropsGroupThirdPartiesIntegrationRancher",
    "CfnGroupPropsGroupThirdPartiesIntegrationRightScale",
    "CfnGroupPropsGroupThirdPartiesIntegrationRoute53",
    "CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains",
    "CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets",
    "Dimension",
    "DockerSwarm",
    "DockerSwarmAutoScale",
    "Ecs",
    "EcsAutoScale",
    "EcsBatch",
    "EcsOptimizeImages",
    "Headroom",
    "Kubernetes",
    "KubernetesAutoScale",
    "KubernetesAutoScaleHeadroom",
    "KubernetesAutoScaleResourceLimits",
    "LoadBalancerConfig",
    "LoadBalancersConfig",
    "Nomad",
    "NomadAutoScale",
    "ResourceRequirement",
    "ResourceTagSpecificationConfig",
    "ScaleDownAction",
    "ScaleDownStepAdjustment",
    "ScaleUpAction",
    "ScaleUpStepAdjustment",
    "ScalingDownPolicy",
    "ScalingTargetPolicy",
    "ScalingTargetPolicyPredictive",
    "ScalingUpPolicy",
    "Tag",
    "Task",
    "TlsConfig",
]

publication.publish()

def _typecheckingstub__9478cc4b27b054d3ffa8d22ecfb7e1d41ca962813698f0f602875c1fc537d688(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759f59664e992b5203ff390202cc7fd008d4a185c523c3d8a3884ae137b66d70(
    *,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    max_scale_down_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ac0186c8a145a597deb9b32c8b76bef21257e67d3a1ad963e803e2f3ae9f02(
    *,
    action: typing.Optional[builtins.str] = None,
    should_drain_instances: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dde2b7b9f057e6a4056311f29fd57ec58a1a8363155c7695fd24057b666b9f(
    *,
    device_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[BlockDeviceMappingEbs, typing.Dict[builtins.str, typing.Any]]] = None,
    no_device: typing.Optional[builtins.str] = None,
    virtual_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c10ac981f599a2044252842b6ffbb099615349100cfb1361cd6e2bdd512022(
    *,
    delete_on_termination: typing.Optional[builtins.bool] = None,
    dynamic_volume_size: typing.Optional[typing.Union[BlockDeviceMappingEbsDynamicVolumeSize, typing.Dict[builtins.str, typing.Any]]] = None,
    encrypted: typing.Optional[builtins.bool] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[BlockDeviceMappingEbsVolumeType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b9b60e72321319ce12124b3d90ceadc1a8e2d7961b00b52512fa9d591f28b5(
    *,
    base_size: typing.Optional[jsii.Number] = None,
    resource: typing.Optional[builtins.str] = None,
    size_per_resource_unit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e0a0cd3b8949c7f43b677824dc627fa20df44be75a759d4b20a225cc4e0d3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    credentials: typing.Union[CfnGroupPropsCredentials, typing.Dict[builtins.str, typing.Any]],
    group: typing.Optional[typing.Union[CfnGroupPropsGroup, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82575e10378d1e80a2be695e0a4451974db65b6b7371f3a9c5206a6ada5b6571(
    *,
    credentials: typing.Union[CfnGroupPropsCredentials, typing.Dict[builtins.str, typing.Any]],
    group: typing.Optional[typing.Union[CfnGroupPropsGroup, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0c275b3c48a48d155c02caed86b6136e593b75b08a89b188a1b6de40a12bad(
    *,
    access_token: typing.Optional[builtins.str] = None,
    account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2da0e1ca2dea5cefa49b31a4b41756489368be15ebc8431dd8794b542eff90(
    *,
    capacity: typing.Optional[typing.Union[CfnGroupPropsGroupCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    compute: typing.Optional[typing.Union[CfnGroupPropsGroupCompute, typing.Dict[builtins.str, typing.Any]]] = None,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[CfnGroupPropsGroupScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduling: typing.Optional[typing.Union[CfnGroupPropsGroupScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    strategy: typing.Optional[typing.Union[CfnGroupPropsGroupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    third_parties_integration: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    updated_at: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894230b9753e3d68cf11052e16e651cb0d621f7121db214f2ed21c08b9080912(
    *,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
    target: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da077a38f05e3993b1b12bb0749e466d5f318dc90e57119b8d468044262f7994(
    *,
    availability_zones: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeAvailabilityZones, typing.Dict[builtins.str, typing.Any]]]] = None,
    ebs_volume_pool: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeEbsVolumePool, typing.Dict[builtins.str, typing.Any]]]] = None,
    elastic_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_types: typing.Optional[typing.Union[CfnGroupPropsGroupComputeInstanceTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    launch_specification: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    product: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_attachments: typing.Optional[typing.Union[CfnGroupPropsGroupComputeVolumeAttachments, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5d0ec8dfd5c0d0d2321774c8c961748b40c0360c961e6adc738d3f4b6edff7(
    *,
    name: typing.Optional[builtins.str] = None,
    placement_group_name: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d595bbc30a37ff454566ec57e1717051bf4b1ef2ef5b8dba29f650a37337c672(
    *,
    device_name: typing.Optional[builtins.str] = None,
    volume_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1927a0c9607121c4d10644386828ab615815e17301dd36b4b7478e6b8f2c41c5(
    *,
    on_demand: typing.Optional[builtins.str] = None,
    on_demand_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_spot: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_requirements: typing.Optional[typing.Union[CfnGroupPropsGroupComputeInstanceTypesResourceRequirements, typing.Dict[builtins.str, typing.Any]]] = None,
    spot: typing.Optional[typing.Sequence[builtins.str]] = None,
    weights: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeInstanceTypesWeights, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36d674982e3043c79c6f1ceef49201554fb37010c8ec36445cd8338b1ed5743(
    *,
    excluded_instance_families: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_gpu: typing.Optional[typing.Union[ResourceRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    required_memory: typing.Optional[typing.Union[ResourceRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    required_v_cpu: typing.Optional[typing.Union[ResourceRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e79661dd516b26fbee632de105989cfc60917b924e8957e9c70d547c3e174ee(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    weighted_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eee7380e54403b9ce880f4d67b7075395a3a7149abf51a88f9e1a9e846bc266(
    *,
    auto_healing: typing.Optional[builtins.bool] = None,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[BlockDeviceMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
    cpu_options: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationCpuOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    credit_specification: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationCreditSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_optimized: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[jsii.Number] = None,
    health_check_type: typing.Optional[builtins.str] = None,
    health_check_unhealthy_duration_before_replacement: typing.Optional[jsii.Number] = None,
    iam_role: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationIamRole, typing.Dict[builtins.str, typing.Any]]] = None,
    image_id: typing.Optional[builtins.str] = None,
    images: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationImages, typing.Dict[builtins.str, typing.Any]]]] = None,
    itf: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItf, typing.Dict[builtins.str, typing.Any]]] = None,
    key_pair: typing.Optional[builtins.str] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    load_balancer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    load_balancers_config: typing.Optional[typing.Union[LoadBalancersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata_options: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationMetadataOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[builtins.bool] = None,
    network_interfaces: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_tag_specification: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationResourceTagSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    shutdown_script: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tenancy: typing.Optional[builtins.str] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb835b550016d6f85ff299683788b082d41d5acb85f3e613f39b5dd648d2c6d(
    *,
    threads_per_core: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aaa874b619453995216e0ab10da8f9687217431dcb5d0d3957bef2dda4a73b0(
    *,
    cpu_credits: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aca8cb410a3729539a4a314dbce75c50198f529ee196a1999bc9f9ca52c6be1(
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d3299795f9fcec237855c957088013fbee6c78c61a938a457a31c9e0ccb6bd(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755e4bc12352443d3bf7d30e63693ab166a298dcf9df4b22a4bee336329636ce(
    *,
    fixed_target_groups: typing.Optional[builtins.bool] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancers, typing.Dict[builtins.str, typing.Any]]]] = None,
    migration_healthiness_threshold: typing.Optional[jsii.Number] = None,
    target_group_config: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    weight_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da34d258e3d231f155198dc801d0e0e7b0d74a701b7bdaebec2583d6b1744e9(
    *,
    default_static_target_groups: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersDefaultStaticTargetGroups, typing.Dict[builtins.str, typing.Any]]]] = None,
    listener_rules: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRules, typing.Dict[builtins.str, typing.Any]]]] = None,
    load_balancer_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3484dacc0debdccf903c8b49867491c27b66ef678a67bfab25c49a0fdf7b1ba(
    *,
    arn: typing.Optional[builtins.str] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02be5086ed9796560b802f79651646b6581bef0468fbdabae12b2f4f09e00daf(
    *,
    rule_arn: typing.Optional[builtins.str] = None,
    static_target_groups: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItfLoadBalancersListenerRulesStaticTargetGroups, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e67bacc6146f93adb7153121dd549336b5b85e3fcadd270994cda590b60d1b(
    *,
    arn: typing.Optional[builtins.str] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cddfa8eebc74f96bc1d30574ec0f3e129eaf92f0d0a0114c225577edcd2b547(
    *,
    health_check_interval_seconds: typing.Optional[jsii.Number] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    health_check_port: typing.Optional[builtins.str] = None,
    health_check_protocol: typing.Optional[builtins.str] = None,
    health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
    healthy_threshold_count: typing.Optional[jsii.Number] = None,
    matcher: typing.Optional[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationItfTargetGroupConfigMatcher, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd96ef5b5f304f7cd57803c659afe1a5db8d6553f6e3600e6d48f2c4eeaa6f4(
    *,
    grpc_code: typing.Optional[builtins.str] = None,
    http_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248f070286d3763d0f0acb05a72a7684ebdd247f462aa510288dd92b22cab5fb(
    *,
    http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    http_tokens: typing.Optional[builtins.str] = None,
    instance_metadata_tags: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce5482d06528a4cfa6e3e0d548e8ce44c6c6c3b600486889b2ed9e4a94d8c33(
    *,
    associate_ipv6_address: typing.Optional[builtins.bool] = None,
    associate_public_ip_address: typing.Optional[builtins.bool] = None,
    delete_on_termination: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    device_index: typing.Optional[jsii.Number] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interface_id: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    private_ip_addresses: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeLaunchSpecificationNetworkInterfacesPrivateIpAddresses, typing.Dict[builtins.str, typing.Any]]]] = None,
    secondary_private_ip_address_count: typing.Optional[jsii.Number] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b572230f72340b340b156d8cca3073db997c155a9219e03ee56b5f53e2b0cba8(
    *,
    primary: typing.Optional[builtins.bool] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486bebec6c5f0f761ff3d18d12926295a9cddccfe34e63af6eb26a0608458f4f(
    *,
    amis: typing.Optional[typing.Union[ResourceTagSpecificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enis: typing.Optional[typing.Union[ResourceTagSpecificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshots: typing.Optional[typing.Union[ResourceTagSpecificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    volumes: typing.Optional[typing.Union[ResourceTagSpecificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db4a1b4732e973cec3c4efa25eb7a533b3368e4e6ccda3f84131673be460955(
    *,
    volumes: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupComputeVolumeAttachmentsVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc60095e42a0f481392dc4e1a9ca724c35a1f20cf970c053ab78ed058810d67(
    *,
    device_name: typing.Optional[builtins.str] = None,
    volume_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e7511661618b1dbaa7841f92e9a1536c3d91439dc5014d69abc3c56f74b20a(
    *,
    down: typing.Optional[typing.Sequence[typing.Union[ScalingDownPolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
    multiple_metrics: typing.Optional[typing.Union[CfnGroupPropsGroupScalingMultipleMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Sequence[typing.Union[ScalingTargetPolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
    up: typing.Optional[typing.Sequence[typing.Union[ScalingUpPolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3740a569878fe77a5936cfba34ad35082ecc70d259b87ab379dfa73af32ff6fe(
    *,
    expressions: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupScalingMultipleMetricsExpressions, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupScalingMultipleMetricsMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef8c249c69d9a691c607f7980de65f28217355a31ba5467d351a4efb50024d4(
    *,
    expression: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaa82ccf9841e7d166c767bd3bbf234152016d8c22303f203ade70e0f3d48ac(
    *,
    dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33064e0dd49716025f7b3360d1ddec0a63f1d66b443a255fc6d554cf749d13a1(
    *,
    tasks: typing.Optional[typing.Sequence[typing.Union[Task, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2da4975b53bf256b867c857027268e918b39c0a7635f118b55815b2ee4f887(
    *,
    availability_vs_cost: typing.Optional[builtins.str] = None,
    consider_od_pricing: typing.Optional[builtins.bool] = None,
    draining_timeout: typing.Optional[jsii.Number] = None,
    fallback_to_od: typing.Optional[builtins.bool] = None,
    immediate_od_recover_threshold: typing.Optional[jsii.Number] = None,
    lifetime_period: typing.Optional[builtins.str] = None,
    on_demand_count: typing.Optional[jsii.Number] = None,
    persistence: typing.Optional[typing.Union[CfnGroupPropsGroupStrategyPersistence, typing.Dict[builtins.str, typing.Any]]] = None,
    restrict_single_az: typing.Optional[builtins.bool] = None,
    revert_to_spot: typing.Optional[typing.Union[CfnGroupPropsGroupStrategyRevertToSpot, typing.Dict[builtins.str, typing.Any]]] = None,
    risk: typing.Optional[jsii.Number] = None,
    scaling_strategy: typing.Optional[typing.Union[CfnGroupPropsGroupStrategyScalingStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    signals: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupStrategySignals, typing.Dict[builtins.str, typing.Any]]]] = None,
    spin_up_time: typing.Optional[jsii.Number] = None,
    utilize_commitments: typing.Optional[builtins.bool] = None,
    utilize_reserved_instances: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b297029ffe121286b26d9465f36540fafd3ec99a3844b506301b58e1ff49487(
    *,
    block_devices_mode: typing.Optional[builtins.str] = None,
    should_persist_block_devices: typing.Optional[builtins.bool] = None,
    should_persist_private_ip: typing.Optional[builtins.bool] = None,
    should_persist_root_device: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4038443c669504fd62a7fe192dbd44e2b8f11183a61aeabb8503bd9d99393812(
    *,
    perform_at: typing.Optional[builtins.str] = None,
    time_windows: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c4ea38972417a6e950105298c25794fd879cf0cab3a44304bbd342cb72329b(
    *,
    terminate_at_end_of_billing_hour: typing.Optional[builtins.bool] = None,
    termination_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6fa076e7565d225c699363134fe3687bb029836ecfe7edf06e241246bd4dfc(
    *,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5555d4f9d204203ac07f07c71c7c81553d8076fdf497aa0a812e17238a23a8(
    *,
    chef: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationChef, typing.Dict[builtins.str, typing.Any]]] = None,
    code_deploy: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationCodeDeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_swarm: typing.Optional[typing.Union[DockerSwarm, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs: typing.Optional[typing.Union[Ecs, typing.Dict[builtins.str, typing.Any]]] = None,
    elastic_beanstalk: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalk, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationGitlab, typing.Dict[builtins.str, typing.Any]]] = None,
    jenkins: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationJenkins, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes: typing.Optional[typing.Union[Kubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    mesosphere: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationMesosphere, typing.Dict[builtins.str, typing.Any]]] = None,
    mlb_runtime: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationMlbRuntime, typing.Dict[builtins.str, typing.Any]]] = None,
    nomad: typing.Optional[typing.Union[Nomad, typing.Dict[builtins.str, typing.Any]]] = None,
    ops_works: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationOpsWorks, typing.Dict[builtins.str, typing.Any]]] = None,
    rancher: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationRancher, typing.Dict[builtins.str, typing.Any]]] = None,
    right_scale: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationRightScale, typing.Dict[builtins.str, typing.Any]]] = None,
    route53: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationRoute53, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8ab428ecf44992772678cee610d0647301230bc713d19ada85eb16bf1b283d(
    *,
    chef_server: typing.Optional[builtins.str] = None,
    chef_version: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    pem_key: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd7671b9bec15a81fe403e32e96b93775bc11f0ef34ed74ddc45c7d34bfb247(
    *,
    clean_up_on_failure: typing.Optional[builtins.bool] = None,
    deployment_groups: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationCodeDeployDeploymentGroups, typing.Dict[builtins.str, typing.Any]]]] = None,
    terminate_instance_on_failure: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332a3aceba069d7e5c5c597c6e06d2938fbf30f33f38e6949539f8cbc776be68(
    *,
    application_name: typing.Optional[builtins.str] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d131c237712829165735ac4ee4ed29626b1fa1ce7b039982556375fca808cd(
    *,
    id: typing.Optional[builtins.str] = None,
    metrics_to_report: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationDatadogMetricsToReport, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81102ecd411438dc28cfa28d178d5e8ec04731a39c218af6f947b73523d711e(
    *,
    metrics_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ab9b6815b14d0047e40577bff74c2428d454b73f6903a2e7db435e0b4e434d(
    *,
    deployment_preferences: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkDeploymentPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_id: typing.Optional[builtins.str] = None,
    managed_actions: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9853dcdedddfcb098eb174885dd0adcc3ccbd7f17b16408ca9414b10a0f73a5(
    *,
    automatic_roll: typing.Optional[builtins.bool] = None,
    batch_size_percentage: typing.Optional[jsii.Number] = None,
    grace_period: typing.Optional[jsii.Number] = None,
    strategy: typing.Optional[typing.Union[BeanStalkStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec5285bd3f6d02d365044c8106f9da7c0b0513810adf92179f602697429d50c(
    *,
    platform_update: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationElasticBeanstalkManagedActionsPlatformUpdate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34c3a0df419b8708f1c6a95da6774af5e4b10e22ef10fbbe04430361e619828(
    *,
    instance_refresh_enabled: typing.Optional[builtins.bool] = None,
    perform_at: typing.Optional[builtins.str] = None,
    time_window: typing.Optional[builtins.str] = None,
    update_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfee26a2ab04a4b287dc6b512a93fcec187f22a51a54979560b0757189b633a(
    *,
    runner: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationGitlabRunner, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec04634d1252a709db9e252467b2f36438ffcf23e3ce6db6966e680f763368b6(
    *,
    is_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3eec9f2efab166b23d53e0fcb0a2048ebb58877a12f770ce9ff0c8005cec3d(
    *,
    connection_method: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethod, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b322341fefccaa1dbeb4f7bf234cf26b12698142426ff1dca4acaa9e9d378a8(
    *,
    jnlp: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodJnlp, typing.Dict[builtins.str, typing.Any]]] = None,
    manually_connection: typing.Optional[builtins.bool] = None,
    ssh: typing.Optional[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationJenkinsConnectionMethodSsh, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2083d3376cfd70d24c4d470e08c26370cf05fa9624999d265863af3986359be7(
    *,
    master_ip: typing.Optional[builtins.str] = None,
    master_port: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea48e69031699e0e4e8a84781cbaab80d140f3f9ff9d08124634ba65b8a1016(
    *,
    ssh_public_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4db328a799f95f0060615a6510b435a68af1b6753c104945aca17944574f343(
    *,
    api_server: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46be76a5581f65142ef80b58da02fa335a158862d3e6d4c7ba7106bc8d9b89a(
    *,
    deployment_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12778848891ca597f38262063a51c782da69e0d4deb0845f19c821d0e1add0e(
    *,
    layer_id: typing.Optional[builtins.str] = None,
    stack_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe57865056b712b1203733a620af0c22146831c27c3c778b096af044c1d0ecf(
    *,
    access_key: typing.Optional[builtins.str] = None,
    master_host: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7611add7b872b59867fac77c98f26b9d1cacc6398b8c5554ee470334f28acd(
    *,
    account_id: typing.Optional[builtins.str] = None,
    refresh_token: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91e02e5dec3c5e28d39ef2f85de9f0d848d41aafa47995b9518218e4ac29311(
    *,
    domains: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationRoute53Domains, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8c1d153188d5f73fb2870c92acbd09c410dea5e6d93d195cbd36c80f468e25(
    *,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    record_sets: typing.Optional[typing.Sequence[typing.Union[CfnGroupPropsGroupThirdPartiesIntegrationRoute53DomainsRecordSets, typing.Dict[builtins.str, typing.Any]]]] = None,
    record_set_type: typing.Optional[builtins.str] = None,
    spotinst_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a47d3270e9dea2522bb94845522a92c7b7215d7c7c71978e76162d3f2e87979(
    *,
    name: typing.Optional[builtins.str] = None,
    use_public_dns: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b163980c9edf9068b97ebe8273844308a50a56a73f7eb96604b080ddac8537(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87debdc2b90d72dd4d8a6277c3f23483225db7b3ea2d5f2c5d29a707ab27192(
    *,
    auto_scale: typing.Optional[typing.Union[DockerSwarmAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    master_host: typing.Optional[builtins.str] = None,
    master_port: typing.Optional[jsii.Number] = None,
    tls_config: typing.Optional[typing.Union[TlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f417a27165b638fad84a8a1385c18ec8f7d05ac162ea2b393e73109b8de96de8(
    *,
    cooldown: typing.Optional[jsii.Number] = None,
    down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
    headroom: typing.Optional[typing.Union[Headroom, typing.Dict[builtins.str, typing.Any]]] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466b61f9eb0052a5d9d806629bab4e13e48e193ee86a917a331cf4ad3efe11b0(
    *,
    auto_scale: typing.Optional[typing.Union[EcsAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    batch: typing.Optional[typing.Union[EcsBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    optimize_images: typing.Optional[typing.Union[EcsOptimizeImages, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960c14eaf1e43efcff09a331d7e0c8ca3f5d02188737bb2497e50d7975d15f03(
    *,
    attributes: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
    cooldown: typing.Optional[jsii.Number] = None,
    down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
    headroom: typing.Optional[typing.Union[Headroom, typing.Dict[builtins.str, typing.Any]]] = None,
    is_auto_config: typing.Optional[builtins.bool] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
    should_scale_down_non_service_tasks: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3264a75640a8edad557155e40074f9fd12451cf509ae5a20917902a0e1042b1(
    *,
    job_queue_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f70955dc6486d6e50bba46be0b08edd3f15932703fda1aab9edd609df0a9e38(
    *,
    perform_at: typing.Optional[builtins.str] = None,
    should_optimize_ecs_ami: typing.Optional[builtins.bool] = None,
    time_windows: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e986fe251c74bfbb246d8a4b74d8a3e00fc39a66b560a75d2d1b1d54c3cacc0c(
    *,
    cpu_per_unit: typing.Optional[jsii.Number] = None,
    memory_per_unit: typing.Optional[jsii.Number] = None,
    num_of_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3694c1c971f6eb09e76cd892ae70e4ce646c4ef0d7dabbf961ffb6d9e2373ef(
    *,
    api_server: typing.Optional[builtins.str] = None,
    auto_scale: typing.Optional[typing.Union[KubernetesAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    integration_mode: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f111c1c7e1dc537f7e0ede4e5c37c764ed66451e0a389a806d69a95b886162c(
    *,
    cooldown: typing.Optional[jsii.Number] = None,
    down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
    headroom: typing.Optional[typing.Union[KubernetesAutoScaleHeadroom, typing.Dict[builtins.str, typing.Any]]] = None,
    is_auto_config: typing.Optional[builtins.bool] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_limits: typing.Optional[typing.Union[KubernetesAutoScaleResourceLimits, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72787ca4b189c23e71172780dc61cd9da82ae53326c4a729fa374904c8c57bb7(
    *,
    cpu_per_unit: typing.Optional[jsii.Number] = None,
    gpu_per_unit: typing.Optional[jsii.Number] = None,
    memory_per_unit: typing.Optional[jsii.Number] = None,
    num_of_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb9de9d51f10b20b02ef3faf61d8fcf4cec38df4a7fc9da3d3cd842ac881e3a(
    *,
    max_memory_gib: typing.Optional[jsii.Number] = None,
    max_v_cpu: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9853541fd4fef1f9d5344d4945aeacdf8670627a72a96d335c0acce346368f(
    *,
    arn: typing.Optional[builtins.str] = None,
    auto_weight: typing.Optional[builtins.bool] = None,
    az_awareness: typing.Optional[builtins.bool] = None,
    balancer_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    target_set_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74bf1ac7dbb4658a198d974ee4ed79843672d1e3e7cd2943545bcf9286fe236(
    *,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9b3422a120172edbe3288a42b94079fe1e021790658ce6faa7a8cf1b5e0729(
    *,
    acl_token: typing.Optional[builtins.str] = None,
    auto_scale: typing.Optional[typing.Union[NomadAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    master_host: typing.Optional[builtins.str] = None,
    master_port: typing.Optional[jsii.Number] = None,
    tls_config: typing.Optional[typing.Union[TlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45064f0f945dd7cde95702d7ae27abd708fb99e80a05f88db7834b22dbf3e29(
    *,
    constraints: typing.Optional[typing.Sequence[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]]] = None,
    cooldown: typing.Optional[jsii.Number] = None,
    down: typing.Optional[typing.Union[AutoScaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
    headroom: typing.Optional[typing.Union[Headroom, typing.Dict[builtins.str, typing.Any]]] = None,
    is_auto_config: typing.Optional[builtins.bool] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ed0d055209a39f79c800529c0286604f73899b0184585dc587389d4f4c56a6(
    *,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b96f5d6f4798f6a974636f73901548e6462df4f6adbf041e83640fa78855d89(
    *,
    should_tag: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48233f1f1ee03947b62a946b093370816c851996acca56d85938f26c74edff44(
    *,
    maximum: typing.Optional[builtins.str] = None,
    minimum: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a501ac3f74b4caa1a7827f6067dbe447c02fed3f7b7806cb6b8962d7ff1d68(
    *,
    action: typing.Optional[typing.Union[ScaleDownAction, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fa7250c0bf2ffa7dcc325e846e7b40a28449aa3f280f17cbc7435179e2c60b(
    *,
    maximum: typing.Optional[builtins.str] = None,
    minimum: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc497ef3fd9fbcbdfeda2c543fabd663139f6e3aadf169885a467d779e809261(
    *,
    action: typing.Optional[typing.Union[ScaleUpAction, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437cfe3caf825521b8a4e6b8b4c80e37560c4229b3945d66ad4e288b56ddac4f(
    *,
    action: typing.Optional[typing.Union[ScaleDownAction, typing.Dict[builtins.str, typing.Any]]] = None,
    cooldown: typing.Optional[jsii.Number] = None,
    dimension: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    policy_name: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    step_adjustments: typing.Optional[typing.Sequence[typing.Union[ScaleDownStepAdjustment, typing.Dict[builtins.str, typing.Any]]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8c641bcf497af93b386b851070f78445dc10e5b6c7f72d7c7d7a9d5cb49f47(
    *,
    cooldown: typing.Optional[jsii.Number] = None,
    dimension: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    max_capacity_per_scale: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    policy_name: typing.Optional[builtins.str] = None,
    predictive: typing.Optional[typing.Union[ScalingTargetPolicyPredictive, typing.Dict[builtins.str, typing.Any]]] = None,
    source: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    target: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ddc90adc76ff6fc7505c5219d0dd35decd6a46991a5f95ad01ba57b174313c(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ce11ffeeda21d567628540e9dd295211ef4ccbcd8dab40741388e140cfffbf(
    *,
    action: typing.Optional[typing.Union[ScaleUpAction, typing.Dict[builtins.str, typing.Any]]] = None,
    cooldown: typing.Optional[jsii.Number] = None,
    dimension: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    policy_name: typing.Optional[builtins.str] = None,
    should_resume_stateful: typing.Optional[builtins.bool] = None,
    source: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    step_adjustments: typing.Optional[typing.Sequence[typing.Union[ScaleUpStepAdjustment, typing.Dict[builtins.str, typing.Any]]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba768e6ef5a62c63e7aadaf97eae5cb36a88ad2361f245b7acce6300e8b8674a(
    *,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b6b735b15d3de623e7f51f851353aee987008f8fdb1a3dda95a881fe0689a7(
    *,
    adjustment: typing.Optional[jsii.Number] = None,
    adjustment_percentage: typing.Optional[jsii.Number] = None,
    batch_size_percentage: typing.Optional[jsii.Number] = None,
    cron_expression: typing.Optional[builtins.str] = None,
    frequency: typing.Optional[builtins.str] = None,
    grace_period: typing.Optional[jsii.Number] = None,
    is_enabled: typing.Optional[builtins.bool] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    scale_max_capacity: typing.Optional[jsii.Number] = None,
    scale_min_capacity: typing.Optional[jsii.Number] = None,
    scale_target_capacity: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    task_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3060f10fbd76d62a140badf76efdd51788d0e051b12ea2203b7a630389571221(
    *,
    certificate: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    tls_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
